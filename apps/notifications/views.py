from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.http import HttpRequest
from django.db.models import Q, Count, F
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import uuid
import logging
from django.db import DatabaseError
from django.contrib.auth import get_user_model
from .models import Notification, UserNotification

logger = logging.getLogger(__name__)
User = get_user_model()

from .models import Notification
# from apps.authentication.models import User

logger = logging.getLogger(__name__)


# def ensure_user(user):
#     """
#     Convert input to a User instance.
#     Accepts:
#       - User instance
#       - UUID object or string
#       - Email string
#     """
#     if isinstance(user, User):
#         return user
#     if isinstance(user, UUID):
#         return User.objects.get(id=user)
#     if isinstance(user, str):
#         # Try as UUID first
#         try:
#             uid = UUID(user)
#             return User.objects.get(id=uid)
#         except (ValueError, User.DoesNotExist):
#             # Treat as email
#             return User.objects.get(email=user)
#     raise ValueError(f"Cannot resolve user: {user}")



@login_required
def notifications_list(request):
    user = request.user
    notifications = UserNotification.objects.filter(user=user).select_related('notification').order_by('-created_at')

    # Filters
    notif_type = request.GET.get('type')
    status = request.GET.get('status')
    time_filter = request.GET.get('time')

    if notif_type:
        notifications = notifications.filter(notification__notification_type=notif_type)
    if status == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status == 'read':
        notifications = notifications.filter(is_read=True)
    if time_filter:
        now = timezone.now()
        if time_filter == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            notifications = notifications.filter(created_at__gte=start)
        elif time_filter == 'week':
            start = now - timedelta(days=7)
            notifications = notifications.filter(created_at__gte=start)
        elif time_filter == 'month':
            start = now - timedelta(days=30)
            notifications = notifications.filter(created_at__gte=start)

    # Pagination
    paginator = Paginator(notifications, 10)  # 10 notifications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Counts for dashboard cards
    total_notifications = UserNotification.objects.filter(user=user).count()
    unread_notifications = UserNotification.objects.filter(user=user, is_read=False).count()
    order_notifications = UserNotification.objects.filter(user=user, notification__notification_type='order').count()
    system_notifications = UserNotification.objects.filter(user=user, notification__notification_type='system').count()

    context = {
        'notifications': page_obj.object_list,
        'page_obj': page_obj,
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'order_notifications': order_notifications,
        'system_notifications': system_notifications,
        'current_type_filter': notif_type or '',
        'current_status_filter': status or '',
        'current_time_filter': time_filter or '',
    }
    return render(request, 'employee/notifications.html', context)


@login_required
def mark_notification_read(request):
        if request.method == 'POST':
            notif_id = request.POST.get('id')
        if not notif_id:
            return HttpResponseBadRequest('Missing ID')
        notif = get_object_or_404(UserNotification, id=notif_id, user=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'success': True})
        return HttpResponseBadRequest('Invalid request method')


@login_required
def delete_notification(request):
    if request.method == 'POST':
        notif_id = request.POST.get('id')
        if not notif_id:
            return HttpResponseBadRequest('Missing ID')
        notif = get_object_or_404(UserNotification, id=notif_id, user=request.user)
        notif.delete()
        return JsonResponse({'success': True})
    return HttpResponseBadRequest('Invalid request method')

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        UserNotification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return HttpResponseBadRequest('Invalid request method')



@login_required
def notification_preferences(request):
    try:
        preferences = NotificationPreference.objects.get(user=request.user)
    except NotificationPreference.DoesNotExist:
        preferences = NotificationPreference.objects.create(
            user=request.user,
            email_enabled=True,
            push_enabled=True,
            order_notifications=True,
            payment_notifications=True,
            menu_notifications=True,
            system_notifications=True
        )
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            preferences.email_enabled = data.get('email_enabled', preferences.email_enabled)
            preferences.push_enabled = data.get('push_enabled', preferences.push_enabled)
            preferences.order_notifications = data.get('order_notifications', preferences.order_notifications)
            preferences.payment_notifications = data.get('payment_notifications', preferences.payment_notifications)
            preferences.menu_notifications = data.get('menu_notifications', preferences.menu_notifications)
            preferences.system_notifications = data.get('system_notifications', preferences.system_notifications)
            preferences.save()
            return JsonResponse({
                'success': True,
                'message': 'Notification preferences updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error updating preferences: {str(e)}'
            }, status=400)
    context = {'preferences': preferences}
    return render(request, 'notifications/preferences.html', context)

# def send_notification(user, title, message, notification_type="system",
#                       priority="normal", action_url=None, action_text=None,
#                       target_audience="all", order=None, request=None):
#     """
#     Simple notification function that works with your existing database
#     Uses the notifications_notification table with target_user_id FK
#     """
#     try:
#         from django.contrib.auth import get_user_model
#         import uuid
        
#         User = get_user_model()
        
#         # Ensure we have a User instance
#         if isinstance(user, str):
#             try:
#                 user_obj = User.objects.get(id=user)
#             except User.DoesNotExist:
#                 user_obj = User.objects.get(email=user)
#         else:
#             user_obj = user

#         # Create notification with explicit is_read=False
#         from .models import Notification
#         notification = Notification.objects.create(
#             id=str(uuid.uuid4()),
#             target_user=user_obj,  # This should match your FK field
#             order=order,
#             created_by=request.user if request and hasattr(request, "user") and request.user.is_authenticated else None,
#             title=title,
#             message=message,
#             notification_type=notification_type,
#             priority=priority,
#             action_url=action_url or "",
#             action_text=action_text or "",
#             target_audience=target_audience,
#             is_read=False  # Explicitly set this
#         )
        
#         logger.info(f"Notification created for user {user_obj.email}: {title}")
#         return notification
        
#     except Exception as e:
#         logger.error(f"Error creating notification for user {user}: {str(e)}", exc_info=True)
#         return None

def send_notification(user, title, message, notification_type="system",
                      priority="normal", action_url=None, action_text=None,
                      target_audience="all", order=None, request=None):
    """
    Create notification in both tables
    """
    try:
        from django.contrib.auth import get_user_model
        import uuid
        
        User = get_user_model()
        
        # Ensure we have a User instance
        if isinstance(user, str):
            try:
                user_obj = User.objects.get(id=user)
            except User.DoesNotExist:
                user_obj = User.objects.get(email=user)
        else:
            user_obj = user

        # Step 1: Create notification in notifications_notification
        notification = Notification.objects.create(
            target_user=user_obj,
            order=order,
            created_by=request.user if request and hasattr(request, "user") and request.user.is_authenticated else None,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            action_url=action_url or "",
            action_text=action_text or "",
            target_audience=target_audience,
            is_read=False
        )
        
        # Step 2: Create link in notifications_usernotification
        user_notification = UserNotification.objects.create(
            user=user_obj,
            notification=notification,
            is_read=False
        )
        
        logger.info(f"✅ Notification created: {notification.id}, UserNotification: {user_notification.id}")
        return notification
        
    except Exception as e:
        logger.error(f"❌ Error creating notification: {str(e)}", exc_info=True)
        return None


def send_bulk_notification(users, title, message, notification_type="system",
                          priority="normal", action_url=None, action_text=None,
                          target_audience="all", order=None, request=None):
    """
    Send notification to multiple users efficiently
    Creates one notification record and multiple UserNotification records
    
    Args:
        users: List of User instances
        Other args same as send_notification
    
    Returns:
        tuple: (success_count, failed_users)
    """
    try:
        # Step 1: Create the main notification once
        notification = Notification.objects.create(
            id=str(uuid.uuid4()),
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            action_url=action_url or "",
            action_text=action_text or "",
            target_audience=target_audience,
            order=order,
            created_by=request.user if request and hasattr(request, "user") and request.user.is_authenticated else None,
            created_at=timezone.now()
        )

        # Step 2: Create UserNotification records for each user
        user_notifications = []
        failed_users = []
        
        for user in users:
            try:
                user_notifications.append(
                    UserNotification(
                        user=user,
                        notification=notification,
                        is_read=False
                    )
                )
            except Exception as e:
                failed_users.append(str(user.id) if hasattr(user, 'id') else str(user))
                logger.warning(f"Failed to prepare notification for user {user}: {e}")

        # Bulk create for efficiency
        UserNotification.objects.bulk_create(user_notifications)
        
        success_count = len(user_notifications)
        logger.info(f"Bulk notification sent to {success_count} users, failed for {len(failed_users)} users")
        
        return success_count, failed_users

    except Exception as e:
        logger.error(f"Error sending bulk notification: {str(e)}", exc_info=True)
        return 0, [str(user.id) if hasattr(user, 'id') else str(user) for user in users]



class SystemNotificationManagementView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'canteen_admin/notifications.html'
    def test_func(self):
        return self.request.user.is_canteen_admin or self.request.user.is_superuser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notification.objects.annotate(recipients_count=Count('target_user')).order_by('-created_at')
        type_filter = self.request.GET.get('type', 'all')
        if type_filter != 'all':
            notifications = notifications.filter(notification_type=type_filter)
        paginator = Paginator(notifications, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update({
            'notifications': page_obj,
            'total_sent': Notification.objects.count(),
            'sent_today': Notification.objects.filter(created_at__date=timezone.now().date()).count(),
            'active_employees': User.objects.filter(is_active=True).count(),
            'scheduled_notifications': 0,  # No scheduling support
            'departments': Department.objects.all(),
            'type_filter': type_filter,
            'status_filter': 'all',  # No status field
        })
        return context

def send_email_notification(user, notification):
    """Send email notification"""
    try:
        # Get email template
        try:
            template = NotificationTemplate.objects.get(
                name=f'email_{notification.notification_type}',
                is_active=True
            )
            subject = template.subject
            html_content = template.render_content({
                'user': user,
                'notification': notification,
                'site_name': 'Enterprise Canteen'
            })
        except NotificationTemplate.DoesNotExist:
            # Use default template
            subject = f'Enterprise Canteen - {notification.title}'
            html_content = render_to_string('notifications/email_template.html', {
                'user': user,
                'notification': notification,
                'site_name': 'Enterprise Canteen'
            })
        
        # Convert to plain text
        plain_message = strip_tags(html_content)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False
        )
        
        logger.info(f'Email notification sent to {user.email}')
        
    except Exception as e:
        logger.error(f'Error sending email notification: {str(e)}')


# def send_bulk_notification(users, title, message, notification_type='info', priority='normal'):
#     """Send notification to multiple users"""
#     try:
#         notifications_created = 0
        
#         for user in users:
#             user_notification = send_notification(
#                 user=user,
#                 title=title,
#                 message=message,
#                 notification_type=notification_type,
#                 priority=priority
#             )
#             if user_notification:
#                 notifications_created += 1
        
#         logger.info(f'Bulk notification sent to {notifications_created} users')
#         return notifications_created
        
#     except Exception as e:
#         logger.error(f'Error sending bulk notification: {str(e)}')
#         return 0


@login_required
@user_passes_test(lambda u: u.is_canteen_admin or u.is_superuser)
def system_notification_management(request):
    notifications = Notification.objects.annotate(
        recipients_count=Count('target_user'),
        status=Case(
            When(is_read=True, then=Value('read')),
            When(is_read=False, then=Value('sent')),
            output_field=CharField()
        )
    ).order_by('-created_at')
    type_filter = request.GET.get('type', 'all')
    if type_filter != 'all':
        notifications = notifications.filter(notification_type=type_filter)
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'notifications': page_obj,
        'total_sent': Notification.objects.filter(is_read=False).count(),
        'sent_today': Notification.objects.filter(created_at__date=timezone.now().date()).count(),
        'active_employees': User.objects.filter(is_active=True).count(),
        'scheduled_notifications': 0,  # No scheduling support
        'departments': Department.objects.all(),
        'type_filter': type_filter,
        'status_filter': 'all',  # Status derived from is_read
    }
    return render(request, 'notifications.html', context)


@login_required
def send_system_notification(request):
    """Send a system-wide or targeted notification from the admin panel."""
    if not (request.user.is_canteen_admin or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body) if request.content_type == "application/json" else request.POST
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        notification_type = data.get('type', 'system')
        target_users = data.get('target_users', 'all')
        department_ids = data.getlist('departments', [])
        send_email = data.get('send_email', False)

        if not title or not message:
            return JsonResponse({'error': 'Title and message are required'}, status=400)

        # Select target users
        if target_users == 'all':
            users = User.objects.filter(is_active=True)
        elif target_users == 'employees' and department_ids:
            users = User.objects.filter(department__id__in=department_ids, is_active=True)
        elif target_users == 'admins':
            users = User.objects.filter(role__in=['canteen_admin', 'system_admin'], is_active=True)
        else:
            return JsonResponse({'error': 'Invalid target users or departments'}, status=400)

        # Send notifications
        sent_count = 0
        for user in users:
            if send_notification(user=user, title=title, message=message,
                                 notification_type=notification_type):
                sent_count += 1
            if send_email:
                # Optional email sending logic here
                pass

        return JsonResponse({
            'success': True,
            'message': f'Notification sent to {sent_count} users',
            'sent_count': sent_count,
            'notification': {
                'title': title,
                'message': message,
                'type': notification_type,
                'created_at': timezone.now().strftime("%Y-%m-%d %H:%M"),
                'recipients': users.count(),
            }
        })

    except Exception as e:
        logger.error(f'Error sending system notification: {str(e)}', exc_info=True)
        return JsonResponse({'error': f'Failed to send notification: {str(e)}'}, status=500)

@login_required
def notification_templates_api(request):
    if not (request.user.is_canteen_admin or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    templates = NotificationTemplate.objects.filter(is_active=True).order_by('title')
    templates_data = [
        {
            'id': str(template.id),
            'title': template.title,
            'message': template.message,
            'notification_type': template.notification_type,
            'created_at': template.created_at.strftime('%Y-%m-%d %H:%M')
        } for template in templates
    ]
    return JsonResponse({'templates': templates_data})

@login_required
def create_notification_template(request):
    if not (request.user.is_canteen_admin or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template = NotificationTemplate.objects.create(
                title=data['title'],
                message=data['message'],
                notification_type=data.get('notification_type', 'system'),
                created_at=timezone.now()
            )
            return JsonResponse({
                'success': True,
                'message': 'Template created successfully',
                'template_id': str(template.id)
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error creating template: {str(e)}'
            }, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def notifications_page(request):
    if not (request.user.is_canteen_admin or request.user.is_superuser):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    notifications = Notification.objects.annotate(recipients_count=Count('recipients')).order_by('-created_at')
    type_filter = request.GET.get('type', 'all')
    status_filter = request.GET.get('status', 'all')
    if type_filter != 'all':
        notifications = notifications.filter(notification_type=type_filter)
    if status_filter != 'all':
        notifications = notifications.filter(status=status_filter)
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'notifications': page_obj,
        'total_sent': Notification.objects.filter(status='sent').count(),
        'sent_today': Notification.objects.filter(status='sent', created_at__date=timezone.now().date()).count(),
        'active_employees': User.objects.filter(is_active=True).count(),
        'scheduled_notifications': Notification.objects.filter(status='scheduled').count(),
        'departments': Department.objects.all(),
        'type_filter': type_filter,
        'status_filter': status_filter,
    }
    return render(request, 'employee/notifications.html', context)

def send_order_notification(order, notification_type, additional_context=None):
    """
    Updated function to work with junction table system
    """
    try:
        user = getattr(order, "customer", None) or getattr(order, "employee", None)
        if not user:
            logger.warning(f"No user found for order {order.id}")
            return None

        # Determine notification content
        if notification_type == 'order_confirmed':
            title = f"Order {order.order_number} Confirmed"
            message = "Your order has been confirmed. Please proceed to payment."
            action_url = f"/orders/{order.id}/payment/"
            action_text = "Proceed to Payment"

        elif notification_type == 'order_ready':
            title = f"Order {order.order_number} Ready"
            message = "Your order is ready for pickup!"
            action_url = f"/orders/{order.id}/detail/"
            action_text = "View Order"

        elif notification_type == 'order_cancelled':
            title = f"Order {order.order_number} Cancelled"
            message = "Your order has been cancelled by the canteen admin."
            action_url = f"/orders/{order.id}/detail/"
            action_text = "View Details"

        elif notification_type == 'order_delayed':
            title = f"Order {order.order_number} Delayed"
            message = "Your order is taking longer than expected. We apologize for the delay."
            action_url = f"/orders/{order.id}/detail/"
            action_text = "View Order"

        else:
            title = f"Order {order.order_number} Update"
            message = "Your order status has been updated."
            action_url = f"/orders/{order.id}/detail/"
            action_text = "View Order"

        # Send notification using the clean system
        return send_notification(
            user=user,
            title=title,
            message=message,
            notification_type='order',
            priority='normal',
            action_url=action_url,
            action_text=action_text,
            target_audience='specific_user',
            order=order
        )

    except Exception as e:
        logger.error(f"Error sending order notification: {str(e)}", exc_info=True)
        return None

def send_payment_notification(payment, notification_type):
    """Send payment-related notifications"""
    try:
        user = payment.user
        
        if notification_type == 'payment_successful':
            if payment.payment_type == 'topup':
                title = 'Wallet Top-up Successful'
                message = f'Your wallet has been topped up with {payment.amount} XAF via {payment.get_payment_method_display()}.'
            else:
                title = 'Payment Successful'
                message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} completed successfully.'
            action_url = '/payments/history/'
            action_text = 'View Payment History'
            
        elif notification_type == 'payment_failed':
            if payment.payment_type == 'topup':
                title = 'Wallet Top-up Failed'
                message = f'Your wallet top-up of {payment.amount} XAF failed. Please try again.'
            else:
                title = 'Payment Failed'
                message = f'Payment of {payment.amount} XAF for order #{payment.order.order_number} failed.'
            action_url = '/payments/history/'
            action_text = 'Try Again'
            
        elif notification_type == 'low_balance':
            title = 'Low Wallet Balance'
            message = f'Your wallet balance is low ({user.wallet_balance} XAF). Consider topping up your wallet.'
            action_url = '/payments/topup/'
            action_text = 'Top Up Wallet'
            
        else:
            title = 'Payment Update'
            message = f'Payment status updated for {payment.amount} XAF.'
            action_url = '/payments/history/'
            action_text = 'View Details'
        
        # Send notification
        return send_notification(
            user=user,
            title=title,
            message=message,
            notification_type='payment',
            action_url=action_url,
            action_text=action_text
        )
        
    except Exception as e:
        logger.error(f'Error sending payment notification: {str(e)}')
        return None


def send_menu_notification(users, notification_type, additional_context=None):
    """Send menu-related notifications"""
    try:
        context = additional_context or {}
        
        if notification_type == 'daily_menu_updated':
            title = 'New Daily Menu Available'
            message = "Today's special menu has been updated with new items and offers!"
            action_url = '/menu/'
            action_text = 'View Menu'
            
        elif notification_type == 'new_item_added':
            item_name = context.get('item_name', 'new item')
            title = 'New Menu Item'
            message = f'Check out our new menu item: {item_name}!'
            action_url = '/menu/'
            action_text = 'View Menu'
            
        elif notification_type == 'special_offer':
            title = 'Special Offer Available'
            message = context.get('message', 'Limited time special offers available!')
            action_url = '/menu/'
            action_text = 'View Offers'
            
        else:
            title = 'Menu Update'
            message = 'The menu has been updated with new items and changes.'
            action_url = '/menu/'
            action_text = 'View Menu'
        
        # Send to multiple users
        sent_count = 0
        for user in users:
            user_notification = send_notification(
                user=user,
                title=title,
                message=message,
                notification_type='menu',
                action_url=action_url,
                action_text=action_text
            )
            if user_notification:
                sent_count += 1
        
        return sent_count
        
    except Exception as e:
        logger.error(f'Error sending menu notifications: {str(e)}')
        return 0


# @login_required
# def get_real_time_notifications(request):
#     """Get real-time notifications for AJAX polling"""
#     # Get notifications created in the last 5 minutes
#     five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
    
#     recent_notifications = UserNotification.objects.filter(
#         user=request.user,
#         created_at__gte=five_minutes_ago,
#         is_read=False
#     ).select_related('notification').order_by('-created_at')
    
#     notifications_data = []
#     for user_notification in recent_notifications:
#         notification = user_notification.notification
#         notifications_data.append({
#             'id': str(user_notification.id),
#             'title': notification.title,
#             'message': notification.message,
#             'type': notification.notification_type,
#             'priority': notification.priority,
#             'created_at': user_notification.created_at.isoformat(),
#             'action_url': notification.action_url,
#             'action_text': notification.action_text
#         })
    
#     return JsonResponse({
#         'notifications': notifications_data,
#         'count': len(notifications_data)
#     })


@login_required
def notification_stats_api(request):
    """API endpoint for notification statistics"""
    if not request.user.is_canteen_admin() and not request.user.is_system_admin():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Overall statistics
    total_notifications = Notification.objects.count()
    unread_notifications = UserNotification.objects.filter(is_read=False).count()
    
    # Today's statistics
    today = timezone.now().date()
    today_notifications = Notification.objects.filter(created_at__date=today).count()
    
    # Notifications by type
    notifications_by_type = Notification.objects.values('notification_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent activity
    recent_activity = Notification.objects.select_related('user').order_by('-created_at')[:5]
    
    recent_data = []
    for notification in recent_activity:
        recent_data.append({
            'title': notification.title,
            'user': notification.user.get_full_name() if notification.user else 'System',
            'type': notification.notification_type,
            'created_at': notification.created_at.strftime('%b %d, %Y at %I:%M %p')
        })
    
    return JsonResponse({
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'today_notifications': today_notifications,
        'notifications_by_type': list(notifications_by_type),
        'recent_activity': recent_data
    })

@login_required
def notifications_page(request):
    if not request.user.is_canteen_admin():
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Base queryset (don’t slice yet)
    notifications_qs = Notification.objects.all().order_by("-created_at")

    # Apply slice ONLY when passing to template (for pagination or limiting)
    notifications = notifications_qs[:20]  # Example: show only 20 latest

    context = {
        "notifications": notifications_qs,
        "total_sent": notifications_qs.count(),
        "sent_today": notifications_qs.filter(created_at__date=timezone.now().date()).count(),
        "active_employees": 42,
        "scheduled_notifications": 0,  # you don’t have scheduling
    }

    return render(request, "employee/notifications.html", context)

@login_required
def notification_count(request):
    try:
        unread_count = UserNotification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return JsonResponse({'success': True, 'unread_count': unread_count})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def fetch_notifications(request):
    user = request.user

    # --- 1. Notifications via UserNotification ---
    linked_qs = (
    UserNotification.objects.filter(user_id=user.id)
    .select_related("notification", "notification__order")
    )
    print("DEBUG linked_qs IDs:", list(linked_qs.values_list("id", flat=True)))


    # --- 2. Direct notifications ---
    direct_qs = Notification.objects.filter(target_user_id=user.id)
    print("DEBUG direct_qs IDs:", list(direct_qs.values_list("id", flat=True)))

    direct_wrapped = [
        UserNotification(
            id=f"direct-{n.id}",
            user=user,
            notification=n,
            is_read=n.is_read,
            created_at=n.created_at,
        )
        for n in direct_qs
    ]

    # --- 3. Combine ---
    all_notifications = list(linked_qs) + direct_wrapped

    # --- 4. Sort ---
    all_notifications.sort(key=lambda x: x.created_at, reverse=True)

    # --- 5. Paginate ---
    paginator = Paginator(all_notifications, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # --- 6. Render partial template ---
    return render(
        request,
        "employee/notifications.html",
        {"notifications": page_obj.object_list, "page_obj": page_obj},
    )
