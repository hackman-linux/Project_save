import requests
import json
import logging
from decimal import Decimal
from django.conf import settings
from typing import Dict, Tuple
import hashlib
import hmac

logger = logging.getLogger(__name__)

class CamPayError(Exception):
    """Custom exception for CamPay API errors"""
    pass

class CamPayService:
    """
    CamPay Payment Service - Alternative Implementation
    Supports both Token-based and API Key authentication
    """
    
    def __init__(self):
        self.config = settings.CAMPAY_CONFIG
        self.base_url = self.config["BASE_URL"]
        self.username = self.config.get("USERNAME", "")
        self.password = self.config.get("PASSWORD", "")
        self.api_key = self.config.get("API_KEY", "")
        self.environment = self.config["ENVIRONMENT"]
        self._cached_token = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers - uses API key if token auth fails"""
        headers = {"Content-Type": "application/json"}
        
        # Try API key first if available
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            return headers
        
        # Otherwise try token authentication
        try:
            token = self._get_auth_token()
            headers["Authorization"] = f"Token {token}"
        except CamPayError as e:
            logger.warning(f"Token auth failed: {e}. Trying API key...")
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            else:
                raise CamPayError("No valid authentication method available")
        
        return headers
    
    def _get_auth_token(self) -> str:
        """Get authentication token (cached for efficiency)"""
        if self._cached_token:
            return self._cached_token
        
        if not self.username or not self.password:
            raise CamPayError(
                "Missing CamPay credentials. Please set USERNAME and PASSWORD in settings."
            )
        
        try:
            auth_url = f"{self.base_url}/api/token/"
            
            payload = {
                "username": self.username,
                "password": self.password
            }
            
            logger.info(f"Authenticating with CamPay at {auth_url}")
            
            response = requests.post(
                auth_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            logger.info(f"Auth response: {response.status_code}")
            
            # Handle non-200 responses
            if response.status_code == 401:
                raise CamPayError(
                    "Invalid CamPay credentials. Check your USERNAME and PASSWORD."
                )
            
            if response.status_code >= 400:
                error_text = response.text[:200]
                raise CamPayError(
                    f"CamPay authentication failed ({response.status_code}): {error_text}"
                )
            
            # Check if response is JSON
            content_type = response.headers.get('Content-Type', '')
            if 'json' not in content_type.lower():
                raise CamPayError(
                    f"CamPay returned non-JSON response. "
                    f"This usually means invalid credentials. Response: {response.text[:200]}"
                )
            
            # Parse response
            try:
                data = response.json()
            except ValueError:
                raise CamPayError(
                    f"Cannot parse CamPay response as JSON: {response.text[:200]}"
                )
            
            token = data.get('token')
            if not token:
                raise CamPayError(f"No token in response: {list(data.keys())}")
            
            self._cached_token = token
            logger.info("CamPay authentication successful")
            return token
            
        except requests.RequestException as e:
            raise CamPayError(f"Network error during authentication: {str(e)}")
    
    def initiate_payment(self, order, phone_number: str, payment_method: str = "campay_mtn") -> Tuple[bool, Dict]:
        """Initiate payment with CamPay"""
        try:
            phone_number = self.format_phone_number(phone_number)
            operator = "MTN" if payment_method == "campay_mtn" else "ORANGE"
            
            payment_data = {
                "amount": str(int(order.total_amount)),
                "from": phone_number,
                "description": f"Order #{order.order_number}",
                "external_reference": str(order.id),
                "operator": operator,
            }
            
            url = f"{self.base_url}/api/collect/"
            headers = self._get_headers()
            
            logger.info(f"Initiating payment: {payment_data}")
            
            response = requests.post(url, json=payment_data, headers=headers, timeout=30)
            
            logger.info(f"Payment response status: {response.status_code}")
            logger.info(f"Payment response: {response.text[:500]}")
            
            # Handle response
            if response.status_code >= 400:
                error_msg = response.text[:200]
                return False, {"error": f"Payment failed ({response.status_code}): {error_msg}"}
            
            try:
                response_data = response.json()
            except ValueError:
                return False, {"error": f"Invalid response: {response.text[:200]}"}
            
            status = response_data.get("status", "").upper()
            
            if status == "PENDING" or status == "SUCCESSFUL":
                return True, {
                    "transaction_id": response_data.get("reference"),
                    "status": status,
                    "operator": operator,
                    "phone_number": phone_number,
                    "amount": order.total_amount,
                    "message": "Payment request sent. Check your phone to approve.",
                    "external_reference": str(order.id)
                }
            else:
                error_msg = response_data.get("message", "Payment failed")
                return False, {"error": error_msg, "details": response_data}
                
        except Exception as e:
            logger.error(f"Payment error: {str(e)}", exc_info=True)
            return False, {"error": str(e)}
    
    def check_payment_status(self, transaction_reference: str) -> Tuple[bool, Dict]:
        """Check payment status"""
        try:
            url = f"{self.base_url}/api/transaction/{transaction_reference}/"
            headers = self._get_headers()
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return True, {
                "reference": data.get("reference"),
                "status": data.get("status"),
                "amount": data.get("amount"),
                "operator": data.get("operator"),
                "external_reference": data.get("external_reference"),
            }
            
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return False, {"error": str(e)}
    
    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number for Cameroon"""
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        if phone_number.startswith("237") and len(phone_number) == 12:
            return phone_number
        elif phone_number.startswith("6") and len(phone_number) == 9:
            return f"237{phone_number}"
        else:
            raise CamPayError(f"Invalid phone number: {phone_number}")
    
    def verify_webhook(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        return True  # Implement proper verification in production
    
    def handle_webhook(self, payload: Dict) -> Dict:
        """Process webhook"""
        return {
            "reference": payload.get("reference"),
            "external_reference": payload.get("external_reference"),
            "status": payload.get("status"),
            "amount": Decimal(str(payload.get("amount", 0))),
            "operator": payload.get("operator"),
        }

# Singleton instance
campay_service = CamPayService()