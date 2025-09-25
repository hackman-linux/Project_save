# notifications/services.py

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import transaction
import logging

from .models import (
    UserNotification, SystemNotification, NotificationPreference,
    NotificationLog, NotificationTemplate
)

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """Main service for handling notifications"""

    @staticmethod
    def create_user_notification(
        user,
        title,
        message,
        notification_type='system_announcement',
        priority='normal',
        order=None,
        action_url='',
        action_text='',
        created_by=None,
        send_channels=None
    ):
        """Create a notification for a specific user"""
        try:
            # Check user preferences
            try:
                preferences = NotificationPreference.objects.get(user=user)
            except NotificationPreference.DoesNotExist:
                preferences = NotificationPreference.objects.create(user=user)

            # Check if user allows this type of notification
            if not preferences.allows_notification_type(notification_type):
                logger.info(f"User {user.username} has disabled {notification_type} notifications")
                return None

            # Create the notification
            notification = UserNotification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                order=order,
                action_url=action_url,
                action_text=action_text,
                created_by=created_by
            )

            # Log in-app notification
            NotificationLog.objects.create(
                user_notification=notification,
                channel='app',
                status='sent'
            )

            # Send via additional channels if requested
            if send_channels:
                if 'email' in send_channels and preferences.email_enabled:
                    NotificationService._send_email_notification(notification)
                
                if 'sms' in send_channels and preferences.sms_enabled:
                    NotificationService._send_sms_notification(notification)

            logger.info(f"Created notification for user {user.username}: {title}")
            return notification

        except Exception as e:
            logger.error(f"Error creating user notification: {str(e)}")
            return None

    @staticmethod
    def create_system_notification(
        title,
        message,
        notification_type='system_announcement',
        priority='normal',
        target_audience='all_employees',
        target_departments=None,
        action_url='',
        action_text='',
        created_by=None,
        scheduled_for=None,
        send_immediately=False
    ):
        """Create a system-wide notification"""
        try:
            with transaction.atomic():
                # Create system notification
                system_notification = SystemNotification.objects.create(
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    priority=priority,
                    target_audience=target_audience,
                    action_url=action_url,
                    action_text=action_text,
                    created_by=created_by,
                    scheduled_for=scheduled_for or timezone.now()
                )

                # Add target departments if specified
                if target_departments:
                    system_notification.target_departments.set(target_departments)

                # Send immediately if requested
                if send_immediately:
                    success = system_notification.send_notification()
                    if success:
                        logger.info(f"System notification sent to {system_notification.sent_count} users")
                    else:
                        logger.error("Failed to send system notification")

                return system_notification

        except Exception as e:
            logger.error(f"Error creating system notification: {str(e)}")
            return None

    @staticmethod
    def send_order_notification(order, notification_type, created_by=None, additional_context=None):
        """Send order-related notification"""
        try:
            context = additional_context or {}
            
            # Get notification template or create default message
            title, message, action_url, action_text = NotificationService._get_order_notification_content(
                order, notification_type, context
            )

            return NotificationService.create_user_notification(
                user=order.employee,
                title=title,
                message=message,
                notification_type=notification_type,
                priority='normal' if notification_type != 'order_cancelled' else 'high',
                order=order,
                action_url=action_url,
                action_text=action_text,
                created_by=created_by,
                send_channels=['email']  # Also send via email for important order updates
            )

        except Exception as e:
            logger.error(f"Error sending order notification: {str(e)}")
            return None

    @staticmethod
    def send_payment_notification(payment, notification_type, created_by=None):
        """Send payment-related notification"""
        try:
            user = payment.user if hasattr(payment, 'user') else payment.order.employee
            
            title, message, action_url, action_text = NotificationService._get_payment_notification_content(
                payment, notification_type
            )

            return NotificationService.create_user_notification(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                priority='normal',
                action_url=action_url,
                action_text=action_text,
                created_by=created_by,
                send_channels=['email']
            )

        except Exception as e:
            logger.error(f"Error sending payment notification: {str(e)}")
            return None

    @staticmethod
    def mark_notification_as_read(notification_id, user):
        """Mark a specific notification as read"""
        try:
            notification = UserNotification.objects.get(id=notification_id, user=user)
            notification.mark_as_read()
            return True
        except UserNotification.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            return False

    @staticmethod
    def mark_all_notifications_as_read(user):
        """Mark all unread notifications as read for a user"""
        try:
            updated = UserNotification.objects.filter(
                user=user, 
                is_read=False,
                is_deleted=False
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            logger.info(f"Marked {updated} notifications as read for user {user.username}")
            return updated
        except Exception as e:
            logger.error(f"Error marking all notifications as read: {str(e)}")
            return 0

    @staticmethod
    def delete_notification(notification_id, user):
        """Soft delete a notification"""
        try:
            notification = UserNotification.objects.get(id=notification_id, user=user)
            notification.soft_delete()
            return True
        except UserNotification.DoesNotExist:
            return False
        except Exception as e:
            logger.error(f"Error deleting notification: {str(e)}")
            return False

    @staticmethod
    def get_user_notifications(user, limit=20, notification_type=None, is_read=None):
        """Get notifications for a user with filtering"""
        try:
            queryset = UserNotification.objects.filter(
                user=user,
                is_deleted=False
            ).select_related('order', 'system_notification')

            if notification_type:
                queryset = queryset.filter(notification_type=notification_type)
            
            if is_read is not None:
                queryset = queryset.filter(is_read=is_read)

            return queryset[:limit]

        except Exception as e:
            logger.error(f"Error getting user notifications: {str(e)}")
            return UserNotification.objects.none()

    @staticmethod
    def get_notification_stats(user):
        """Get notification statistics for a user"""
        try:
            total = UserNotification.objects.filter(user=user, is_deleted=False).count()
            unread = UserNotification.objects.filter(user=user, is_read=False, is_deleted=False).count()
            
            # Count by type
            order_count = UserNotification.objects.filter(
                user=user, 
                notification_type__in=['order_status', 'order_ready', 'order_cancelled'],
                is_deleted=False
            ).count()
            
            system_count = UserNotification.objects.filter(
                user=user,
                notification_type='system_announcement',
                is_deleted=False
            ).count()

            return {
                'total': total,
                'unread': unread,
                'order_notifications': order_count,
                'system_notifications': system_count
            }

        except Exception as e:
            logger.error(f"Error getting notification stats: {str(e)}")
            return {'total': 0, 'unread': 0, 'order_notifications': 0, 'system_notifications': 0}

    @staticmethod
    def _send_email_notification(notification):
        """Send email notification"""
        try:
            if not hasattr(settings, 'EMAIL_HOST') or not settings.DEFAULT_FROM_EMAIL:
                logger.warning("Email settings not configured")
                return False

            # Create email log entry
            log_entry = NotificationLog.objects.create(
                user_notification=notification,
                channel='email',
                status='pending'
            )

            # Prepare email content
            subject = f"Enterprise Canteen - {notification.title}"
            
            # Use template if available
            try:
                html_content = render_to_string('notifications/email/notification.html', {
                    'notification': notification,
                    'user': notification.user
                })
                text_content = strip_tags(html_content)
            except:
                # Fallback to simple text
                html_content = f"""
                <html>
                <body>
                    <h2>{notification.title}</h2>
                    <p>{notification.message}</p>
                    {f'<p><a href="{notification.action_url}">{notification.action_text}</a></p>' if notification.action_url else ''}
                </body>
                </html>
                """
                text_content = f"{notification.title}\n\n{notification.message}"

            # Send email
            send_mail(
                subject=subject,
                message=text_content,
                html_message=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=False
            )

            # Update log
            log_entry.status = 'sent'
            log_entry.save()
            
            logger.info(f"Email sent to {notification.user.email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email notification: {str(e)}")
            # Update log with error
            if 'log_entry' in locals():
                log_entry.status = 'failed'
                log_entry.error_message = str(e)
                log_entry.save()
            return False

    @staticmethod
    def _send_sms_notification(notification):
        """Send SMS notification (placeholder for SMS service integration)"""
        # This would integrate with an SMS service like Twilio, etc.
        logger.info(f"SMS notification would be sent to {notification.user.phone_number}: {notification.title}")
        
        # Create log entry
        NotificationLog.objects.create(
            user_notification=notification,
            channel='sms',
            status='sent'  # Would be 'pending' in real implementation
        )
        return True

    @staticmethod
    def _get_order_notification_content(order, notification_type, context):
        """Get notification content for order notifications"""
        base_url = context.get('base_url', '')
        
        content_map = {
            'order_status': {
                'title': f'Order #{order.order_number} Confirmed',
                'message': f'Your order has been confirmed and is ready for payment. Total: {order.total_amount} XAF',
                'action_url': f'{base_url}/orders/{order.id}/payment/',
                'action_text': 'Pay Now'
            },
            'order_ready': {
                'title': f'Order #{order.order_number} Ready',
                'message': f'Your order is ready for pickup at the canteen!',
                'action_url': f'{base_url}/orders/{order.id}/details/',
                'action_text': 'View Order'
            },
            'order_cancelled': {
                'title': f'Order #{order.order_number} Cancelled',
                'message': f'Your order has been cancelled. {context.get("reason", "")}',
                'action_url': f'{base_url}/orders/{order.id}/details/',
                'action_text': 'View Details'
            },
            'payment_success': {
                'title': f'Payment Confirmed - Order #{order.order_number}',
                'message': f'Payment confirmed! Your order is now being prepared.',
                'action_url': f'{base_url}/orders/{order.id}/details/',
                'action_text': 'Track Order'
            }
        }
        
        content = content_map.get(notification_type, {
            'title': f'Order #{order.order_number} Update',
            'message': f'Your order status has been updated.',
            'action_url': f'{base_url}/orders/{order.id}/details/',
            'action_text': 'View Order'
        })
        
        return content['title'], content['message'], content['action_url'], content['action_text']

    @staticmethod
    def _get_payment_notification_content(payment, notification_type):
        """Get notification content for payment notifications"""
        content_map = {
            'payment_success': {
                'title': 'Payment Successful',
                'message': f'Payment of {payment.amount} XAF completed successfully.',
                'action_url': '/payments/history/',
                'action_text': 'View Payment History'
            },
            'payment_failed': {
                'title': 'Payment Failed',
                'message': f'Payment of {payment.amount} XAF failed. Please try again.',
                'action_url': '/payments/retry/',
                'action_text': 'Try Again'
            },
            'wallet_topup': {
                'title': 'Wallet Top-up Successful',
                'message': f'Your wallet has been topped up with {payment.amount} XAF.',
                'action_url': '/wallet/',
                'action_text': 'View Wallet'
            }
        }
        
        content = content_map.get(notification_type, {
            'title': 'Payment Update',
            'message': f'Payment status updated.',
            'action_url': '/payments/history/',
            'action_text': 'View Details'
        })
        
        return content['title'], content['message'], content['action_url'], content['action_text']


class NotificationScheduler:
    """Service for handling scheduled notifications"""
    
    @staticmethod
    def process_scheduled_notifications():
        """Process notifications that are scheduled to be sent"""
        try:
            now = timezone.now()
            scheduled_notifications = SystemNotification.objects.filter(
                status='scheduled',
                scheduled_for__lte=now
            )
            
            for notification in scheduled_notifications:
                success = notification.send_notification()
                if success:
                    logger.info(f"Processed scheduled notification: {notification.title}")
                else:
                    logger.error(f"Failed to process scheduled notification: {notification.title}")
                    
        except Exception as e:
            logger.error(f"Error processing scheduled notifications: {str(e)}")

    @staticmethod
    def cleanup_old_notifications(days=30):
        """Clean up old read notifications"""
        try:
            cutoff_date = timezone.now() - timezone.timedelta(days=days)
            deleted_count = UserNotification.objects.filter(
                is_read=True,
                created_at__lt=cutoff_date
            ).delete()[0]
            
            logger.info(f"Cleaned up {deleted_count} old notifications")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up notifications: {str(e)}")
            return 0


# Convenience functions for common notification scenarios
def notify_user(user, title, message, **kwargs):
    """Simple function to notify a user"""
    return NotificationService.create_user_notification(
        user=user,
        title=title,
        message=message,
        **kwargs
    )

def notify_order_update(order, notification_type, **kwargs):
    """Simple function to send order notification"""
    return NotificationService.send_order_notification(
        order=order,
        notification_type=notification_type,
        **kwargs
    )

def notify_payment_update(payment, notification_type, **kwargs):
    """Simple function to send payment notification"""
    return NotificationService.send_payment_notification(
        payment=payment,
        notification_type=notification_type,
        **kwargs
    )