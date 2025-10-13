import requests
import logging
import json
from decimal import Decimal
from django.conf import settings
from typing import Dict, Optional
import hashlib
import hmac

logger = logging.getLogger(__name__)


class CamPayError(Exception):
    """Custom exception for CamPay API errors"""
    pass


class CamPayService:
    """
    CamPay Payment Service.
    Supports API Key or Token-based authentication.
    """

    def __init__(self):
        self.config = getattr(settings, "CAMPAY_CONFIG", {})
        self.base_url = self.config.get("BASE_URL", "").rstrip('/')
        self.username = self.config.get("USERNAME", "")
        self.password = self.config.get("PASSWORD", "")
        self.api_key = self.config.get("API_KEY", "")
        self.webhook_secret = self.config.get("WEBHOOK_SECRET", self.api_key)
        self.environment = self.config.get("ENVIRONMENT", "sandbox")
        self._cached_token: Optional[str] = None

    # -----------------------------
    # Authentication & Headers
    # -----------------------------
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests - prioritize API key if available"""
        headers = {"Content-Type": "application/json"}
        
        # If API key is set and not empty, use it directly (no token needed)
        if self.api_key and len(self.api_key) > 10:
            logger.info("Using API Key authentication")
            headers["Authorization"] = f"Token {self.api_key}"
            return headers
        
        # Otherwise, get token via username/password
        logger.info("Using username/password token authentication")
        token = self._get_auth_token()
        headers["Authorization"] = f"Token {token}"
        return headers

    def _get_auth_token(self) -> str:
        """Authenticate and cache token"""
        if self._cached_token:
            return self._cached_token
        if not (self.username and self.password):
            raise CamPayError("Missing CamPay credentials")
        try:
            url = f"{self.base_url}/api/token/"
            payload = {"username": self.username, "password": self.password}
            
            logger.info(f"Attempting authentication at: {url}")
            logger.info(f"Username: {self.username[:10]}...")
            
            resp = requests.post(url, json=payload, timeout=30)
            
            # Log the response for debugging
            logger.info(f"Auth response status: {resp.status_code}")
            logger.info(f"Auth response headers: {dict(resp.headers)}")
            logger.info(f"Auth response body: {resp.text[:500]}")
            
            resp.raise_for_status()
            
            # Try to parse JSON
            try:
                data = resp.json()
            except ValueError as e:
                logger.error(f"Invalid JSON response from CamPay: {resp.text[:200]}")
                raise CamPayError(f"CamPay returned invalid response. Status: {resp.status_code}")
            
            token = data.get("token")
            if not token:
                raise CamPayError(f"No token in response: {data}")
            
            self._cached_token = token
            logger.info("Successfully authenticated with CamPay")
            return token
            
        except requests.HTTPError as e:
            logger.error(f"HTTP error during auth: {e.response.status_code} - {e.response.text[:200]}")
            raise CamPayError(f"Authentication failed: HTTP {e.response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Request error during auth: {e}")
            raise CamPayError(f"Cannot connect to CamPay: {e}")
        except Exception as e:
            logger.error(f"Unexpected auth error: {e}")
            raise CamPayError(f"Authentication error: {e}")

    # -----------------------------
    # Phone Utilities
    # -----------------------------
    def format_phone_number(self, phone_number: str) -> str:
        """Convert local Cameroonian numbers to international format"""
        digits = "".join(filter(str.isdigit, phone_number))
        if digits.startswith("237") and len(digits) == 12:
            return digits
        elif digits.startswith("6") and len(digits) == 9:
            return f"237{digits}"
        raise CamPayError(f"Invalid phone number format: {phone_number}. Expected 9 digits starting with 6, or 12 digits starting with 237")

    # -----------------------------
    # Payment Initiation
    # -----------------------------
    def initiate_payment(self, order, phone_number: str, payment_method: str = "campay_mtn") -> Dict:
        """
        Initiate a payment collection request via CamPay
        
        Args:
            order: Order object with total_amount, order_number, and id
            phone_number: Customer's phone number
            payment_method: Payment method (campay_mtn or campay_orange)
            
        Returns:
            Dict with success status and payment details or error message
        """
        try:
            # Format phone number
            phone_number = self.format_phone_number(phone_number)
            
            # Determine operator
            operator = "MTN" if "mtn" in payment_method.lower() else "ORANGE"

            # Prepare payment data
            payment_data = {
                "amount": str(int(order.total_amount)),  # CamPay requires integer
                "from": phone_number,
                "description": f"Order #{getattr(order, 'order_number', order.id)}",
                "external_reference": str(getattr(order, 'id', order.id)),
                "currency": "XAF",  # Required: Central African CFA franc
            }

            # Build collection URL
            url = f"{self.base_url}/api/collect/"
            headers = self._get_headers()

            logger.info(f"Initiating CamPay payment to {url}")
            logger.info(f"Payment data: {payment_data}")
            
            # Make request
            resp = requests.post(url, json=payment_data, headers=headers, timeout=45)
            
            # Log full response for debugging
            logger.info(f"CamPay response status: {resp.status_code}")
            logger.info(f"CamPay response headers: {dict(resp.headers)}")
            logger.info(f"CamPay response body: {resp.text}")
            
            # Try to raise for status
            try:
                resp.raise_for_status()
            except requests.HTTPError as e:
                logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
                return {"success": False, "error": f"Payment service error: {e.response.text[:100]}"}

            # Parse response
            try:
                data = resp.json()
            except ValueError:
                logger.error(f"Invalid JSON from CamPay: {resp.text[:200]}")
                return {"success": False, "error": "Invalid response from payment service"}
            
            logger.info(f"Parsed CamPay response: {data}")
            
            # CamPay returns different response formats:
            # - If payment initiated: {"reference": "...", "ussd_code": "...", "operator": "..."}
            # - If explicit status: {"reference": "...", "status": "PENDING/SUCCESSFUL/FAILED"}
            
            status = data.get("status", "").upper()
            reference = data.get("reference")
            
            # If we have a reference and no explicit FAILED status, treat as success
            # (Payment was initiated successfully, waiting for user approval)
            if reference and status != "FAILED":
                # Default to PENDING if no status provided
                if not status:
                    status = "PENDING"
                    
                return {
                    "success": True,
                    "data": {
                        "transaction_id": reference,
                        "status": status,
                        "operator": data.get("operator", operator),
                        "phone_number": phone_number,
                        "amount": order.total_amount,
                        "message": data.get("message", "Payment request sent. Check your phone to approve."),
                        "external_reference": str(getattr(order, 'id', order.id)),
                        "ussd_code": data.get("ussd_code", ""),  # Include USSD code
                    },
                }

            # If we reach here, payment explicitly failed
            error_message = (
                data.get("message") or 
                data.get("error") or 
                data.get("reason") or
                f"Payment failed with status: {status}"
            )
            logger.error(f"CamPay payment explicitly failed. Status: {status}")
            logger.error(f"Full CamPay response: {json.dumps(data, indent=2)}")
            
            # Provide helpful error messages
            if status == "FAILED":
                if "insufficient" in error_message.lower():
                    user_message = "Insufficient balance. Please top up your mobile money account."
                elif "invalid" in error_message.lower():
                    user_message = "Invalid phone number or payment details."
                else:
                    user_message = "Payment failed. Please try again or contact support."
            else:
                user_message = error_message
                
            return {"success": False, "error": user_message}
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"CamPay HTTP error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            return {"success": False, "error": f"Payment service error: {e.response.status_code}"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CamPay request error: {e}")
            return {"success": False, "error": "Unable to connect to payment service"}
            
        except CamPayError as e:
            logger.error(f"CamPay error: {e}")
            return {"success": False, "error": str(e)}
            
        except Exception as e:
            logger.exception("Unexpected CamPay error")
            return {"success": False, "error": "An unexpected error occurred"}

    # -----------------------------
    # Payment Status
    # -----------------------------
    def check_payment_status(self, transaction_reference: str) -> Dict:
        """
        Check the status of a payment transaction
        
        Args:
            transaction_reference: The CamPay transaction reference
            
        Returns:
            Dict with success status and transaction data
        """
        try:
            url = f"{self.base_url}/transaction/{transaction_reference}/"
            headers = self._get_headers()
            
            logger.info(f"Checking payment status for: {transaction_reference}")
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            
            data = resp.json()
            logger.info(f"Payment status response: {data}")
            
            return {"success": True, "data": data}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Status check HTTP error: {e.response.status_code} - {e.response.text}")
            return {"success": False, "error": f"Unable to verify payment status"}
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {"success": False, "error": "Unable to verify payment status"}

    # -----------------------------
    # Webhook Handling
    # -----------------------------
    def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify webhook signature
        
        Args:
            payload: Raw webhook payload string
            signature: Signature from X-CamPay-Signature header
            
        Returns:
            bool indicating if signature is valid
        """
        if not self.webhook_secret:
            logger.warning("No webhook secret configured, skipping verification")
            return True
            
        computed_sig = hmac.new(
            key=self.webhook_secret.encode(),
            msg=payload.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        is_valid = hmac.compare_digest(computed_sig, signature)
        
        if not is_valid:
            logger.warning(f"Webhook signature mismatch. Expected: {computed_sig}, Got: {signature}")
            
        return is_valid

    def handle_webhook(self, payload: Dict) -> Dict:
        """
        Process webhook payload and extract transaction data
        
        Args:
            payload: Webhook payload dictionary
            
        Returns:
            Dict with normalized transaction data
        """
        try:
            return {
                "reference": payload.get("reference"),
                "external_reference": payload.get("external_reference"),
                "status": payload.get("status"),
                "amount": Decimal(str(payload.get("amount", 0))),
                "operator": payload.get("operator"),
                "reason": payload.get("reason", ""),
            }
        except Exception as e:
            logger.error(f"Error processing webhook payload: {e}")
            return None


# Singleton instance for easy access
campay_service = CamPayService()