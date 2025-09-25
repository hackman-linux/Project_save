# Create this file: apps/payments/services/campay_service.py

import requests
import json
import logging
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from typing import Dict, Any, Optional, Tuple
import hashlib
import hmac

logger = logging.getLogger(__name__)

class CamPayError(Exception):
    """Custom exception for CamPay API errors"""
    pass

class CamPayService:
    """
    CamPay Payment Service Integration
    Handles both MTN and Orange Money payments through CamPay API
    """
    
    def __init__(self):
        self.config = settings.CAMPAY_CONFIG
        self.base_url = self.config["BASE_URL"]
        self.username = self.config["APP_USERNAME"]
        self.password = self.config["APP_PASSWORD"]
        self.environment = self.config["ENVIRONMENT"]
        self.api_version = self.config.get("API_VERSION", "v1.1")
        
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for CamPay API requests"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Token {self._get_auth_token()}",
        }
    
    def _get_auth_token(self) -> str:
        """
        Get authentication token from CamPay
        In production, you should cache this token since it has an expiration time
        """
        try:
            url = f"{self.base_url}/api/{self.api_version}/auth/"
            payload = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            token = data.get("token")
            
            if not token:
                raise CamPayError("No token received from CamPay auth")
                
            return token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CamPay auth failed: {str(e)}")
            raise CamPayError(f"Authentication failed: {str(e)}")
    
    def initiate_payment(self, order, phone_number: str, payment_method: str = "campay_mtn") -> Tuple[bool, Dict]:
        """
        Initiate payment with CamPay
        
        Args:
            order: Order instance
            phone_number: Customer phone number (format: 237XXXXXXXXX)
            payment_method: Either 'campay_mtn' or 'campay_orange'
            
        Returns:
            Tuple[bool, Dict]: (success, response_data)
        """
        try:
            # Format phone number (ensure it starts with country code)
            if not phone_number.startswith("237"):
                if phone_number.startswith("6"):  # Cameroon mobile numbers start with 6
                    phone_number = f"237{phone_number}"
                else:
                    raise CamPayError("Invalid phone number format")
            
            # Determine operator
            operator = "MTN" if payment_method == "campay_mtn" else "ORANGE"
            
            # Prepare payment data
            payment_data = {
                "amount": str(int(order.total_amount)),  # CamPay expects string, no decimals
                "from": phone_number,
                "description": f"Payment for order #{order.order_number}",
                "external_reference": str(order.id),
                "return_url": self._build_return_url(order),
                "operator": operator,
            }
            
            # Make API request
            url = f"{self.base_url}/api/{self.api_version}/collect/"
            headers = self._get_headers()
            
            logger.info(f"Initiating CamPay payment for order {order.order_number}: {payment_data}")
            
            response = requests.post(url, json=payment_data, headers=headers, timeout=30)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("status") == "PENDING":
                # Payment initiated successfully
                return True, {
                    "transaction_id": response_data.get("reference"),
                    "status": response_data.get("status"),
                    "operator": operator,
                    "phone_number": phone_number,
                    "amount": order.total_amount,
                    "message": f"Payment request sent to {phone_number}. Please check your phone and enter your PIN.",
                    "external_reference": str(order.id)
                }
            else:
                # Payment initiation failed
                error_message = response_data.get("message", "Unknown error")
                logger.error(f"CamPay payment initiation failed: {error_message}")
                return False, {
                    "error": error_message,
                    "status": response_data.get("status", "FAILED"),
                    "details": response_data
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"CamPay API request failed: {str(e)}")
            return False, {"error": f"Network error: {str(e)}"}
        
        except Exception as e:
            logger.error(f"CamPay payment initiation error: {str(e)}")
            return False, {"error": f"Payment initiation failed: {str(e)}"}
    
    def check_payment_status(self, transaction_reference: str) -> Tuple[bool, Dict]:
        """
        Check the status of a payment transaction
        
        Args:
            transaction_reference: CamPay transaction reference
            
        Returns:
            Tuple[bool, Dict]: (success, status_data)
        """
        try:
            url = f"{self.base_url}/api/{self.api_version}/transaction/{transaction_reference}/"
            headers = self._get_headers()
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return True, {
                "reference": data.get("reference"),
                "status": data.get("status"),
                "amount": data.get("amount"),
                "operator": data.get("operator"),
                "phone_number": data.get("from"),
                "external_reference": data.get("external_reference"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CamPay status check failed: {str(e)}")
            return False, {"error": f"Status check failed: {str(e)}"}
    
    def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature from CamPay
        
        Args:
            payload: Raw webhook payload
            signature: Signature from webhook headers
            
        Returns:
            bool: True if signature is valid
        """
        try:
            webhook_secret = self.config.get("WEBHOOK_SECRET", "")
            if not webhook_secret:
                logger.warning("No webhook secret configured")
                return False
            
            # Create HMAC signature
            expected_signature = hmac.new(
                webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Webhook verification error: {str(e)}")
            return False
    
    def handle_webhook(self, payload: Dict) -> Optional[Dict]:
        """
        Process CamPay webhook notification
        
        Args:
            payload: Webhook payload data
            
        Returns:
            Dict: Processed transaction data or None if invalid
        """
        try:
            # Extract transaction details
            transaction_data = {
                "reference": payload.get("reference"),
                "external_reference": payload.get("external_reference"),
                "status": payload.get("status"),
                "amount": Decimal(payload.get("amount", 0)),
                "operator": payload.get("operator"),
                "phone_number": payload.get("from"),
                "created_at": payload.get("created_at"),
                "updated_at": payload.get("updated_at"),
            }
            
            logger.info(f"Processing CamPay webhook: {transaction_data}")
            
            return transaction_data
            
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            return None
    
    def _build_return_url(self, order) -> str:
        """Build return URL for payment completion"""
        # You can customize this based on your frontend setup
        from django.urls import reverse
        from django.contrib.sites.models import Site
        
        try:
            current_site = Site.objects.get_current()
            domain = f"https://{current_site.domain}"
        except:
            domain = "http://localhost:8000"  # Fallback for development
        
        return f"{domain}{reverse('orders:payment_success', kwargs={'order_id': order.id})}"
    
    def format_phone_number(self, phone_number: str) -> str:
        """
        Format phone number for Cameroon
        
        Args:
            phone_number: Input phone number
            
        Returns:
            str: Formatted phone number (237XXXXXXXXX)
        """
        # Remove any non-numeric characters
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Handle different input formats
        if phone_number.startswith("237") and len(phone_number) == 12:
            return phone_number
        elif phone_number.startswith("6") and len(phone_number) == 9:
            return f"237{phone_number}"
        elif phone_number.startswith("2376") and len(phone_number) == 12:
            return phone_number
        else:
            raise CamPayError(f"Invalid phone number format: {phone_number}")
    
    def get_supported_operators(self, phone_number: str) -> str:
        """
        Detect mobile operator from phone number
        
        Args:
            phone_number: Cameroon phone number
            
        Returns:
            str: 'MTN' or 'ORANGE'
        """
        # Remove country code for analysis
        if phone_number.startswith("237"):
            phone_number = phone_number[3:]
        
        # MTN Cameroon prefixes
        mtn_prefixes = ['67', '65', '68', '69', '61']  
        # Orange Cameroon prefixes  
        orange_prefixes = ['69', '66', '65', '64', '63']
        
        prefix = phone_number[:2]
        
        if prefix in mtn_prefixes:
            return "MTN"
        elif prefix in orange_prefixes:
            return "ORANGE"
        else:
            # Default to MTN if unsure
            return "MTN"


# Singleton instance
campay_service = CamPayService()