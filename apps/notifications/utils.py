# utils.py - Notification Utility Functions

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# ============================================
# EMAIL UTILITIES
# ============================================

def test_email_connection(config):
    """
    Test SMTP connection with provided configuration
    
    Args:
        config: SystemConfiguration instance
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if not config.smtp_server or not config.smtp_port:
            return False, "SMTP server and port are required"
        
        if not config.smtp_username or not config.smtp_password:
            return False, "SMTP username and password are required"
        
        # Try to connect to SMTP server
        if config.smtp_use_ssl:
            server = smtplib.SMTP_SSL(config.smtp_server, config.smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10)
            if config.smtp_use_tls:
                server.starttls()
        
        # Try to login
        server.login(config.smtp_username, config.smtp_password)
        server.quit()
        
        logger.info(f"Email connection test successful for {config.smtp_server}")
        return True, "SMTP connection successful"
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "SMTP authentication failed. Please check username and password."
        logger.error(f"Email connection test failed: {error_msg}")
        return False, error_msg
        
    except smtplib.SMTPConnectError:
        error_msg = "Could not connect to SMTP server. Please check server address and port."
        logger.error(f"Email connection test failed: {error_msg}")
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Connection test failed: {str(e)}"
        logger.error(f"Email connection test failed: {error_msg}")
        return False, error_msg


def send_test_email(to_email, config):
    """
    Send a test email to verify configuration
    
    Args:
        to_email: Recipient email address
        config: SystemConfiguration instance
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = f"Test Email from {config.app_name}"
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .success-icon {{ font-size: 48px; text-align: center; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✓ Email Configuration Test</h1>
                </div>
                <div class="content">
                    <div class="success-icon">✉️</div>
                    <h2 style="color: #28a745; text-align: center;">Success!</h2>
                    <p>This is a test email from <strong>{config.app_name}</strong>.</p>
                    <p>If you're receiving this email, your email configuration is working correctly.</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3>Configuration Details:</h3>
                        <ul>
                            <li><strong>SMTP Server:</strong> {config.smtp_server}</li>
                            <li><strong>Port:</strong> {config.smtp_port}</li>
                            <li><strong>From Email:</strong> {config.from_email}</li>
                            <li><strong>TLS/SSL:</strong> {'TLS' if config.smtp_use_tls else 'SSL' if config.smtp_use_ssl else 'None'}</li>
                        </ul>
                    </div>
                    
                    <p style="color: #6c757d; font-size: 14px;">
                        <strong>Note:</strong> This is an automated test message. 
                        You can now safely use email notifications in your system.
                    </p>
                </div>
                <div class="footer">
                    <p>Sent from {config.app_name} | System Configuration Test</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.from_email
        msg['To'] = to_email
        
        # Attach HTML content
        html_part = MIMEText(html_message, 'html')
        msg.attach(html_part)
        
        # Send email
        if config.smtp_use_ssl:
            server = smtplib.SMTP_SSL(config.smtp_server, config.smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10)
            if config.smtp_use_tls:
                server.starttls()
        
        server.login(config.smtp_username, config.smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Test email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send test email: {str(e)}")
        return False


def send_notification_email(to_email, subject, message, config, html_message=None):
    """
    Send notification email using system configuration
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        message: Plain text message
        config: SystemConfiguration instance
        html_message: Optional HTML version of the message
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not config.email_enabled:
        logger.warning("Email notifications are disabled")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.from_email
        msg['To'] = to_email
        
        # Attach plain text
        text_part = MIMEText(message, 'plain')
        msg.attach(text_part)
        
        # Attach HTML if provided
        if html_message:
            html_part = MIMEText(html_message, 'html')
            msg.attach(html_part)
        
        # Send email
        if config.smtp_use_ssl:
            server = smtplib.SMTP_SSL(config.smtp_server, config.smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(config.smtp_server, config.smtp_port, timeout=10)
            if config.smtp_use_tls:
                server.starttls()
        
        server.login(config.smtp_username, config.smtp_password)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Notification email sent to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send notification email: {str(e)}")
        return False


# ============================================
# SMS UTILITIES (TWILIO)
# ============================================

def test_sms_connection(config):
    """
    Test Twilio SMS configuration
    
    Args:
        config: SystemConfiguration instance
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from twilio.rest import Client
        
        if not config.twilio_account_sid or not config.twilio_auth_token:
            return False, "Twilio Account SID and Auth Token are required"
        
        if not config.sms_from_number:
            return False, "SMS from number is required"
        
        # Try to create Twilio client
        client = Client(config.twilio_account_sid, config.twilio_auth_token)
        
        # Test by fetching account info
        account = client.api.accounts(config.twilio_account_sid).fetch()
        
        if account.status == 'active':
            logger.info("Twilio connection test successful")
            return True, "Twilio connection successful"
        else:
            return False, f"Twilio account status: {account.status}"
        
    except ImportError:
        error_msg = "Twilio library not installed. Run: pip install twilio"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Twilio connection test failed: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


def send_test_sms(to_phone, config):
    """
    Send a test SMS to verify Twilio configuration
    
    Args:
        to_phone: Recipient phone number (E.164 format)
        config: SystemConfiguration instance
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from twilio.rest import Client
        
        # Ensure phone number is in E.164 format
        if not to_phone.startswith('+'):
            to_phone = '+' + to_phone
        
        # Create Twilio client
        client = Client(config.twilio_account_sid, config.twilio_auth_token)
        
        # Send test message
        message_body = f"Test SMS from {config.app_name}. Your SMS configuration is working correctly!"
        
        message = client.messages.create(
            body=message_body,
            from_=config.sms_from_number,
            to=to_phone
        )
        
        if message.sid:
            logger.info(f"Test SMS sent successfully to {to_phone}. SID: {message.sid}")
            return True, f"SMS sent successfully! Message SID: {message.sid}"
        else:
            return False, "Failed to send SMS"
        
    except ImportError:
        error_msg = "Twilio library not installed. Run: pip install twilio"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Failed to send test SMS: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


def send_notification_sms(to_phone, message, config):
    """
    Send notification SMS using Twilio
    
    Args:
        to_phone: Recipient phone number (E.164 format)
        message: SMS message text
        config: SystemConfiguration instance
        
    Returns:
        tuple: (success: bool, message_sid: str or error: str)
    """
    if not config.sms_enabled:
        logger.warning("SMS notifications are disabled")
        return False, "SMS notifications are disabled"
    
    try:
        from twilio.rest import Client
        
        # Ensure phone number is in E.164 format
        if not to_phone.startswith('+'):
            to_phone = '+' + to_phone
        
        # Create Twilio client
        client = Client(config.twilio_account_sid, config.twilio_auth_token)
        
        # Send message
        sms = client.messages.create(
            body=message,
            from_=config.sms_from_number,
            to=to_phone
        )
        
        if sms.sid:
            logger.info(f"Notification SMS sent to {to_phone}. SID: {sms.sid}")
            return True, sms.sid
        else:
            return False, "Failed to send SMS"
        
    except Exception as e:
        error_msg = f"Failed to send notification SMS: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


# ============================================
# NOTIFICATION HELPERS
# ============================================

def send_order_notification(order, notification_type, config):
    """
    Send order-related notification via email and/or SMS
    
    Args:
        order: Order instance
        notification_type: Type of notification ('placed', 'ready', 'cancelled')
        config: SystemConfiguration instance
        
    Returns:
        dict: Status of email and SMS notifications
    """
    user = order.user
    results = {'email': False, 'sms': False}
    
    # Email notification
    if config.email_enabled and config.notify_order_placed:
        subject = f"Order #{order.order_number} - {notification_type.title()}"
        
        if notification_type == 'placed':
            message = f"Your order #{order.order_number} has been placed successfully. Total: {order.total_amount} XAF"
        elif notification_type == 'ready':
            message = f"Your order #{order.order_number} is ready for pickup!"
        elif notification_type == 'cancelled':
            message = f"Your order #{order.order_number} has been cancelled."
        else:
            message = f"Order #{order.order_number} status update"
        
        results['email'] = send_notification_email(
            to_email=user.email,
            subject=subject,
            message=message,
            config=config
        )
    
    # SMS notification
    if config.sms_enabled and hasattr(user, 'profile') and user.profile.phone_number:
        if notification_type == 'placed' and config.notify_order_placed:
            sms_message = f"Order #{order.order_number} placed. Total: {order.total_amount} XAF. Thank you!"
        elif notification_type == 'ready' and config.notify_order_ready:
            sms_message = f"Your order #{order.order_number} is ready for pickup at {config.app_name}!"
        elif notification_type == 'cancelled':
            sms_message = f"Order #{order.order_number} has been cancelled. Contact us for details."
        else:
            sms_message = None
        
        if sms_message:
            success, _ = send_notification_sms(
                to_phone=user.profile.phone_number,
                message=sms_message,
                config=config
            )
            results['sms'] = success
    
    return results


def send_payment_notification(payment, config):
    """
    Send payment confirmation notification
    
    Args:
        payment: Payment instance
        config: SystemConfiguration instance
        
    Returns:
        dict: Status of email and SMS notifications
    """
    if not config.notify_payment_success:
        return {'email': False, 'sms': False}
    
    user = payment.order.user
    results = {'email': False, 'sms': False}
    
    # Email notification
    if config.email_enabled:
        subject = f"Payment Confirmation - Order #{payment.order.order_number}"
        message = f"""
        Payment received successfully!
        
        Order Number: {payment.order.order_number}
        Amount: {payment.amount} XAF
        Payment Method: {payment.payment_method}
        Transaction ID: {payment.transaction_id}
        
        Thank you for your payment!
        """
        
        results['email'] = send_notification_email(
            to_email=user.email,
            subject=subject,
            message=message,
            config=config
        )
    
    # SMS notification
    if config.sms_enabled and hasattr(user, 'profile') and user.profile.phone_number:
        sms_message = f"Payment of {payment.amount} XAF received for order #{payment.order.order_number}. Thank you!"
        
        success, _ = send_notification_sms(
            to_phone=user.profile.phone_number,
            message=sms_message,
            config=config
        )
        results['sms'] = success
    
    return results


# ============================================
# CONFIGURATION PRESETS
# ============================================

EMAIL_PRESETS = {
    'gmail': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'smtp_use_tls': True,
        'smtp_use_ssl': False,
    },
    'outlook': {
        'smtp_server': 'smtp-mail.outlook.com',
        'smtp_port': 587,
        'smtp_use_tls': True,
        'smtp_use_ssl': False,
    },
    'yahoo': {
        'smtp_server': 'smtp.mail.yahoo.com',
        'smtp_port': 587,
        'smtp_use_tls': True,
        'smtp_use_ssl': False,
    },
    'sendgrid': {
        'smtp_server': 'smtp.sendgrid.net',
        'smtp_port': 587,
        'smtp_use_tls': True,
        'smtp_use_ssl': False,
    },
}


def get_email_preset(provider):
    """
    Get email configuration preset for common providers
    
    Args:
        provider: Email provider name ('gmail', 'outlook', 'yahoo', 'sendgrid')
        
    Returns:
        dict: Configuration preset or None
    """
    return EMAIL_PRESETS.get(provider.lower())