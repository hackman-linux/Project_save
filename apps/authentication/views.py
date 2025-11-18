from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.db.models import Count, Sum, Q, Avg
from datetime import datetime, timedelta
from decimal import Decimal
from .models import SystemConfig

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
import json

from apps.reports.models import AuditLog

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import User, UserActivity
from apps.orders.models import Order, OrderItem
from apps.menu.models import MenuItem, MenuCategory
from apps.payments.models import Payment, WalletTransaction
from apps.notifications.models import Notification

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
import json
import io
import logging

from .models import SystemConfig
from apps.notifications.utils import (
    test_email_connection,
    send_test_email,
    test_sms_connection,
    send_test_sms,
    EMAIL_PRESETS
)

logger = logging.getLogger(__name__)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.role == "system_admin")
def filter_users(request):
    search = request.GET.get("search", "").strip()
    role = request.GET.get("role", "")
    status = request.GET.get("status", "")

    users = CustomUser.objects.all()

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if role:
        users = users.filter(role=role)

    if status:
        if status == "active":
            users = users.filter(is_active=True)
        elif status == "inactive":
            users = users.filter(is_active=False)

    users_html = render_to_string(
        "system_admin/user_table_body.html",
        {"users": users},
        request=request
    )

    return JsonResponse({
        "html": users_html,
        "count": users.count(),
    })


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    html = render_to_string("system_admin/user_details.html", {"u": user})
    return JsonResponse({"html": html})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.department = request.POST.get("department")
        user.save()
        return JsonResponse({"success": True})
    html = render_to_string("system_admin/edit_user_form.html", {"u": user})
    return JsonResponse({"html": html})

@csrf_exempt
def reset_user_password(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        data = json.loads(request.body)
        user.password = make_password(data.get("password"))
        user.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"})

def user_bulk_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ids = data.get("ids", [])
        action = data.get("action")
        users = User.objects.filter(id__in=ids)

        if action == "activate":
            users.update(is_active=True)
        elif action == "deactivate":
            users.update(is_active=False)
        elif action == "delete":
            users.delete()

        return JsonResponse({"success": True, "count": len(ids)})
    return JsonResponse({"success": False})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")  # will be "on" if checked

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if remember_me:
                # Persistent session (e.g., 2 weeks)
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                # Session ends when browser closes
                request.session.set_expiry(0)

            return redirect("dashboard")  # or wherever you want
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")

def contact_admin_reset(request):
    # Simple page telling user to contact system admin
    return render(request, "auth/contact_admin_reset.html")

def is_canteen_admin(self):
    """Check if user is canteen admin"""
    return hasattr(self, 'role') and self.role == 'canteen_admin'

def is_employee(self):
    """Check if user is employee"""
    return hasattr(self, 'role') and self.role == 'employee'


class DashboardRedirectView(LoginRequiredMixin, View):
    """Redirect users to appropriate dashboard based on role"""
    
    def get(self, request):
        user = request.user
        if user.is_system_admin():
            return redirect('system_admin:dashboard')
        elif user.is_canteen_admin():
            return redirect('canteen_admin:dashboard')
        else:
            return redirect('employee:dashboard')


# Employee Dashboard Views
class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Employee dashboard with personal stats and quick actions"""
    template_name = 'employee/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_employee() or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        # Current orders (active orders)
        current_orders = Order.objects.filter(
            employee=user,
            status__in=['pending', 'confirmed', 'preparing', 'ready']
        ).order_by('-created_at')
        
        # Monthly statistics
        monthly_orders = Order.objects.filter(
            employee=user,
            created_at__date__gte=this_month
        ).count()
        
        # Personal statistics
        context.update({
            'current_orders_count': current_orders.count(),
            'monthly_orders': monthly_orders,
            'wallet_balance': user.wallet_balance,
            'favorite_items_count': user.favorite_items.count(),
            'current_orders': current_orders,
            'user': user,
        })
        
        # Today's specials
        todays_specials = MenuItem.objects.filter(
            is_special=True,
            is_available=True,
            special_until__gte=timezone.now()
        )[:4]
        context['todays_specials'] = todays_specials
        
        # Recent notifications
        recent_notifications = Notification.objects.filter(
            target_user=user
        ).select_related('target_user').order_by('-created_at')[:5]
        context['recent_notifications'] = recent_notifications
        
        # Unread notifications count
        unread_notifications = Notification.objects.filter(
            target_user=user,
            is_read=False
        ).count()
        context['unread_notifications'] = unread_notifications
        
        return context

def notifications_list(request):
    return render(request, "employee/notifications.html") 


def profile_view(request):
    return render(request, "auth/profile.html")  


def settings_view(request):
    return render(request, "auth/settings.html")  

def logout_confirm_view(request):
    """Show confirmation page before logout"""
    return render(request, "auth/logout.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("auth/login.html")
    



class CanteenAdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Canteen admin dashboard with operational overview"""
    template_name = 'canteen_admin/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_canteen_admin() or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Today's statistics
        todays_orders = Order.objects.filter(created_at__date=today)
        completed_orders = todays_orders.filter(status='completed')
        
        todays_revenue = completed_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        pending_orders = todays_orders.filter(
            status__in=['pending', 'confirmed', 'preparing']
        ).count()
        
        # Yesterday's comparison
        yesterday_orders = Order.objects.filter(created_at__date=yesterday).count()
        yesterday_revenue = Order.objects.filter(
            created_at__date=yesterday,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        
        # Calculate percentage changes
        orders_change = 0
        if yesterday_orders > 0:
            orders_change = ((todays_orders.count() - yesterday_orders) / yesterday_orders) * 100
        
        revenue_percentage = 0
        if yesterday_revenue > 0:
            revenue_percentage = ((todays_revenue - yesterday_revenue) / yesterday_revenue) * 100
        
        # Low stock items
        low_stock_items = MenuItem.objects.filter(
            current_stock__lte=models.F('low_stock_threshold'),
            is_available=True
        ).count()
        
        # Average preparation time
        avg_prep_time = completed_orders.filter(
            actual_prep_time__isnull=False
        ).aggregate(avg=Avg('actual_prep_time'))['avg'] or 0
        
        # Daily target (example: 50 orders per day)
        daily_target = 50
        
        context.update({
            'todays_orders': todays_orders.count(),
            'todays_revenue': todays_revenue,
            'pending_orders': pending_orders,
            'low_stock_items': low_stock_items,
            'orders_change': orders_change,
            'daily_target': daily_target,
            'revenue_percentage': revenue_percentage,
            'avg_prep_time': avg_prep_time,
        })
        
        # Pending orders list for queue management
        pending_order_list = todays_orders.filter(
            status__in=['confirmed', 'preparing']
        ).select_related('customer').order_by('created_at')[:10]
        context['pending_order_list'] = pending_order_list
        
        # Additional stats for the dashboard
        active_employees = User.objects.filter(
            role='employee',
            status='active',
            last_activity__date=today
        ).count()
        
        # Average order completion time
        avg_order_time = completed_orders.filter(
            validated_at__isnull=False,
            paid_at__isnull=False
        ).annotate(
            completion_time=models.F('paid_at') - models.F('validated_at')
        ).aggregate(avg=Avg('completion_time'))['avg']
        
        if avg_order_time:
            avg_order_time = avg_order_time.total_seconds() / 60  # Convert to minutes
        else:
            avg_order_time = 0
        
        # Orders per hour calculation
        current_hour = timezone.now().hour
        orders_this_hour = todays_orders.filter(
            created_at__hour=current_hour
        ).count()
        
        # Completion rate
        completion_rate = 0
        if todays_orders.count() > 0:
            completion_rate = (completed_orders.count() / todays_orders.count()) * 100
        
        context.update({
            'active_employees': active_employees,
            'avg_order_time': round(avg_order_time, 1),
            'orders_per_hour': orders_this_hour,
            'completion_rate': round(completion_rate, 1),
        })
        
        # Top menu items
        top_menu_items = MenuItem.objects.filter(
            order_items__order__created_at__date=today,
            order_items__order__status='completed'
        ).annotate(
            orders_count=Count('order_items'),
            revenue=Sum(models.F('order_items__quantity') * models.F('order_items__unit_price'))
        ).order_by('-orders_count')[:5]
        context['top_menu_items'] = top_menu_items
        
        # Alerts
        alerts = []
        if low_stock_items > 0:
            alerts.append({
                'type': 'warning',
                'message': f'{low_stock_items} items are running low on stock'
            })
        if pending_orders > 10:
            alerts.append({
                'type': 'danger',
                'message': f'{pending_orders} orders are waiting to be processed'
            })
        context['alerts'] = alerts
        
        # Recent orders for the table
        recent_orders = todays_orders.select_related('customer').order_by('-created_at')[:10]
        context['recent_orders'] = recent_orders
        
        return context


class SystemAdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """System admin dashboard for user management"""
    template_name = 'system_admin/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_system_admin() or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # User statistics
        total_users = User.objects.count()
        employees_count = User.objects.filter(role='employee').count()
        canteen_admins_count = User.objects.filter(role='canteen_admin').count()
        active_users_count = User.objects.filter(status='active').count()
        
        context.update({
            'total_users': total_users,
            'employees_count': employees_count,
            'canteen_admins_count': canteen_admins_count,
            'active_users_count': active_users_count,
        })
        
        # Users list with search and filtering
        users_queryset = User.objects.select_related().order_by('-date_joined')
        
        # Apply filters if provided
        search = self.request.GET.get('search', '')
        role_filter = self.request.GET.get('role', '')
        status_filter = self.request.GET.get('status', '')
        
        if search:
            users_queryset = users_queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(employee_id__icontains=search)
            )
        
        if role_filter:
            users_queryset = users_queryset.filter(role=role_filter)
        
        if status_filter:
            users_queryset = users_queryset.filter(status=status_filter)
        
        context['users'] = users_queryset[:50]  # Limit for performance
        context['search'] = search
        context['role_filter'] = role_filter
        context['status_filter'] = status_filter
        
        return context

User = get_user_model()


# -------------------------
# User Management Dashboard
# -------------------------
def UserManagementView(request):
    """System Admin - Manage Users"""

    # Statistics
    total_users = User.objects.count()
    employees_count = User.objects.filter(role="employee").count()
    canteen_admins_count = User.objects.filter(role="canteen_admin").count()
    active_users_count = User.objects.filter(is_active=True).count()

    # List all users
    users = User.objects.all().order_by("-date_joined")

    context = {
        "total_users": total_users,
        "employees_count": employees_count,
        "canteen_admins_count": canteen_admins_count,
        "active_users_count": active_users_count,
        "users": users,
    }
    return render(request, "system_admin/user_management.html", context)


# -------------------------
# Create User
# -------------------------
def create_user_view(request):
    """System Admin - Create new user"""
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")  
        employee_id = request.POST.get("employee_id")
        department = request.POST.get("department")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if not (first_name and last_name and username and email and phone_number and role and password):
            messages.error(request, "All required fields must be filled.")
            return redirect("system_admin:user_management")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("system_admin:user_management")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("system_admin:user_management")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("system_admin:user_management")

        if User.objects.filter(phone_number=phone_number).exists():  
            messages.error(request, "Phone number already exists.")
            return redirect("system_admin:user_management")

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,  # ✅ saved
            employee_id=employee_id,
            department=department,
            role=role,
            password=make_password(password),
            is_active=True,
        )

        messages.success(request, f"User {user.get_full_name()} created successfully.")
        return redirect("system_admin:user_management")

    return redirect("system_admin:user_management")

def is_system_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == "system_admin")


def audit_logs_view(request):
    today = now().date()
    logs = AuditLog.objects.select_related("user").order_by("-timestamp")[:200]

    context = {
        "audit_logs": logs,
        "total_activities": AuditLog.objects.count(),
        "today_events": AuditLog.objects.filter(timestamp__date=today).count(),
        "active_users": AuditLog.objects.filter(timestamp__date=today).values("user").distinct().count(),
        "failed_logins": AuditLog.objects.filter(activity_type="failed_login", timestamp__date=today).count(),
    }
    return render(request, "audit_logs.html", context)


# Authentication Views
# Updated login_view function in views.py

def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        # Already logged in, redirect by role
        if request.user.is_superuser or request.user.role == "system_admin":
            return redirect("system_admin:dashboard")
        elif request.user.role == "canteen_admin":
            return redirect("canteen_admin:dashboard")
        elif request.user.role == "employee":
            return redirect("employee:dashboard")
        else:
            return redirect("dashboard")

    if request.method == 'POST':
        # Get username (can be email or actual username)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Try authentication
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if account is locked
                if user.is_account_locked():
                    messages.error(request, 'Account is temporarily locked due to multiple failed login attempts.')
                    return render(request, 'auth/login.html')
                
                # Check if account is active
                if user.status != 'active':
                    messages.error(request, 'Your account is not active. Please contact administrator.')
                    return render(request, 'auth/login.html')
                
                # Login successful
                login(request, user)
                user.increment_login_count()
                user.update_last_activity()

                # Log user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description='User logged in successfully',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                # Success message
                messages.success(request, f'Welcome back, {user.get_full_name()}!')

                # Redirect based on 'next' parameter or user role
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)

                # Role-based redirect
                if user.is_superuser or user.role == "system_admin":
                    return redirect("system_admin:dashboard")
                elif user.role == "canteen_admin":
                    return redirect("canteen_admin:dashboard")
                elif user.role == "employee":
                    return redirect("employee:dashboard")
                else:
                    return redirect("dashboard")

            else:
                # Authentication failed
                # Try to find user to increment failed attempts
                try:
                    # Try to find user by email or username
                    from django.db.models import Q
                    failed_user = User.objects.get(
                        Q(email=username) | Q(username=username)
                    )
                    failed_user.increment_failed_login()
                    
                    # Log failed attempt
                    UserActivity.objects.create(
                        user=failed_user,
                        activity_type='login',
                        description='Failed login attempt',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                except User.DoesNotExist:
                    pass
                
                messages.error(request, 'Invalid credentials. Please check your username and password.')
        else:
            messages.error(request, 'Please provide both username and password.')

    return render(request, 'auth/login.html')



@login_required
def logout_view(request):
    """Custom logout view"""
    user = request.user
    
    # Log user activity
    UserActivity.objects.create(
        user=user,
        activity_type='logout',
        description='User logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('auth:login')


# AJAX Views for real-time updates
@login_required
def refresh_employee_orders(request):
    """AJAX view to refresh employee orders"""
    if not request.user.is_employee():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    current_orders = Order.objects.filter(
        customer=request.user,
        status__in=['pending', 'confirmed', 'preparing', 'ready']
    ).select_related('customer').prefetch_related('items__menu_item')
    
    orders_data = []
    for order in current_orders:
        orders_data.append({
            'id': str(order.id),
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'total_amount': str(order.total_amount),
            'created_at': order.created_at.strftime('%H:%M'),
            'can_cancel': order.can_be_cancelled(),
            'items_count': order.get_items_count(),
        })
    
    return JsonResponse({
        'orders': orders_data,
        'count': len(orders_data)
    })


@login_required
def canteen_admin_dashboard_data(request):
    """AJAX view for canteen admin dashboard real-time data"""
    if not request.user.is_canteen_admin():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    today = timezone.now().date()
    todays_orders = Order.objects.filter(created_at__date=today)
    
    data = {
        'todays_orders': todays_orders.count(),
        'pending_orders': todays_orders.filter(
            status__in=['pending', 'confirmed', 'preparing']
        ).count(),
        'completed_orders': todays_orders.filter(status='completed').count(),
        'todays_revenue': str(todays_orders.filter(
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0),
    }
    
    return JsonResponse(data)

@login_required
@user_passes_test(is_system_admin)
def system_config(request):
    """System configuration page for system admins"""
    config, created = SystemConfig.objects.get_or_create(id=1)
    
    context = {
        'config': config,
        'email_presets': EMAIL_PRESETS,
    }
    
    return render(request, "system_admin/system_config.html", context)


# Utility functions
def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Error handlers
def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)


def custom_403(request, exception):
    """Custom 403 error handler"""
    return render(request, 'errors/403.html', status=403)

def language_switcher(request):
    return render(request, "language_switcher.html", {"redirect_to": request.GET.get("next", "/")})

@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def save_config(request):
    """Save system configuration"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        config, _ = SystemConfig.objects.get_or_create(id=1)
        
        # Parse JSON or form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # General Settings
        if 'app_name' in data:
            config.app_name = data['app_name']
        if 'timezone' in data:
            config.timezone = data['timezone']
        if 'currency' in data:
            config.currency = data['currency']
        if 'language' in data:
            config.language = data['language']
        
        # Business Settings
        if 'opening_time' in data:
            config.opening_time = data['opening_time']
        if 'closing_time' in data:
            config.closing_time = data['closing_time']
        if 'order_processing_time' in data:
            config.order_processing_time = int(data['order_processing_time'])
        if 'max_daily_orders' in data:
            config.max_daily_orders = int(data['max_daily_orders'])
        if 'cancellation_window' in data:
            config.cancellation_window = int(data['cancellation_window'])
        config.allow_advance_orders = data.get('allow_advance_orders', 'off') == 'on'
        
        # Payment Settings
        config.mtn_enabled = data.get('mtn_enabled', 'off') == 'on'
        if 'mtn_api_key' in data:
            config.mtn_api_key = data['mtn_api_key']
        if 'mtn_merchant_id' in data:
            config.mtn_merchant_id = data['mtn_merchant_id']
        if 'mtn_environment' in data:
            config.mtn_environment = data['mtn_environment']
        
        config.orange_enabled = data.get('orange_enabled', 'off') == 'on'
        if 'orange_api_key' in data:
            config.orange_api_key = data['orange_api_key']
        if 'orange_merchant_id' in data:
            config.orange_merchant_id = data['orange_merchant_id']
        if 'orange_environment' in data:
            config.orange_environment = data['orange_environment']
        
        if 'payment_timeout' in data:
            config.payment_timeout = int(data['payment_timeout'])
        if 'transaction_fee' in data:
            config.transaction_fee = Decimal(data['transaction_fee'])
        if 'min_order_amount' in data:
            config.min_order_amount = Decimal(data['min_order_amount'])
        config.auto_refund = data.get('auto_refund', 'off') == 'on'
        
        # Email Settings
        config.email_enabled = data.get('email_enabled', 'off') == 'on'
        if 'smtp_server' in data:
            config.smtp_server = data['smtp_server']
        if 'smtp_port' in data:
            config.smtp_port = int(data['smtp_port'])
        if 'from_email' in data:
            config.from_email = data['from_email']
        if 'smtp_username' in data:
            config.smtp_username = data['smtp_username']
        if 'smtp_password' in data and data['smtp_password']:
            config.smtp_password = data['smtp_password']
        config.smtp_use_tls = data.get('smtp_use_tls', 'off') == 'on'
        config.smtp_use_ssl = data.get('smtp_use_ssl', 'off') == 'on'
        
        # SMS Settings
        config.sms_enabled = data.get('sms_enabled', 'off') == 'on'
        if 'sms_provider' in data:
            config.sms_provider = data['sms_provider']
        if 'twilio_account_sid' in data:
            config.twilio_account_sid = data['twilio_account_sid']
        if 'twilio_auth_token' in data and data['twilio_auth_token']:
            config.twilio_auth_token = data['twilio_auth_token']
        if 'sms_from_number' in data:
            config.sms_from_number = data['sms_from_number']
        
        # Push Notifications
        config.push_enabled = data.get('push_enabled', 'off') == 'on'
        if 'firebase_server_key' in data and data['firebase_server_key']:
            config.firebase_server_key = data['firebase_server_key']
        
        # Notification Preferences
        config.notify_order_placed = data.get('notify_order_placed', 'off') == 'on'
        config.notify_order_ready = data.get('notify_order_ready', 'off') == 'on'
        config.notify_payment_success = data.get('notify_payment_success', 'off') == 'on'
        
        # Security Settings
        if 'session_timeout' in data:
            config.session_timeout = int(data['session_timeout'])
        if 'password_min_length' in data:
            config.password_min_length = int(data['password_min_length'])
        config.require_uppercase = data.get('require_uppercase', 'off') == 'on'
        config.require_numbers = data.get('require_numbers', 'off') == 'on'
        config.require_special_chars = data.get('require_special_chars', 'off') == 'on'
        if 'max_login_attempts' in data:
            config.max_login_attempts = int(data['max_login_attempts'])
        if 'lockout_duration' in data:
            config.lockout_duration = int(data['lockout_duration'])
        config.enable_2fa = data.get('enable_2fa', 'off') == 'on'
        config.log_security_events = data.get('log_security_events', 'off') == 'on'
        config.require_password_change = data.get('require_password_change', 'off') == 'on'
        
        # Maintenance Settings
        config.auto_backup = data.get('auto_backup', 'off') == 'on'
        if 'backup_frequency' in data:
            config.backup_frequency = data['backup_frequency']
        if 'backup_time' in data:
            config.backup_time = data['backup_time']
        if 'backup_retention' in data:
            config.backup_retention = int(data['backup_retention'])
        config.performance_monitoring = data.get('performance_monitoring', 'off') == 'on'
        if 'log_level' in data:
            config.log_level = data['log_level']
        if 'log_retention' in data:
            config.log_retention = int(data['log_retention'])
        config.email_alerts = data.get('email_alerts', 'off') == 'on'
        config.maintenance_mode = data.get('maintenance_mode', 'off') == 'on'
        if 'maintenance_message' in data:
            config.maintenance_message = data['maintenance_message']
        
        config.save()
        
        logger.info(f"System configuration updated by {request.user.email}")
        
        return JsonResponse({
            'success': True,
            'message': 'Configuration saved successfully',
            'updated_at': config.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error saving configuration: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def reset_config(request):
    """Reset configuration to defaults"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        # Delete existing config
        SystemConfig.objects.filter(id=1).delete()
        
        # Create new default config
        config = SystemConfig.objects.create(id=1)
        
        logger.info(f"System configuration reset to defaults by {request.user.email}")
        
        return JsonResponse({
            'success': True,
            'message': 'Configuration reset to defaults successfully'
        })
        
    except Exception as e:
        logger.error(f"Error resetting configuration: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error resetting configuration: {str(e)}'
        }, status=400)


@login_required
@user_passes_test(is_system_admin)
def export_config(request):
    """Export configuration as JSON"""
    try:
        config = SystemConfig.objects.get(id=1)
        
        # Create export data
        export_data = {
            'exported_at': timezone.now().isoformat(),
            'exported_by': request.user.email,
            'config': {
                'app_name': config.app_name,
                'app_version': config.app_version,
                'timezone': config.timezone,
                'currency': config.currency,
                'language': config.language,
                'opening_time': str(config.opening_time),
                'closing_time': str(config.closing_time),
                'order_processing_time': config.order_processing_time,
                'max_daily_orders': config.max_daily_orders,
                'cancellation_window': config.cancellation_window,
                'allow_advance_orders': config.allow_advance_orders,
                # Add other fields as needed (excluding sensitive data)
            }
        }
        
        # Create JSON file
        json_data = json.dumps(export_data, indent=2)
        
        # Create response
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="system_config_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
        
        logger.info(f"System configuration exported by {request.user.email}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting configuration: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error exporting configuration: {str(e)}'
        }, status=400)

@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def test_email_config(request):
    """Test email configuration"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        config = SystemConfig.objects.get(id=1)
        
        # Test connection
        success, message = test_email_connection(config)
        
        if success:
            logger.info(f"Email connection test successful by {request.user.email}")
            return JsonResponse({
                'success': True,
                'message': message
            })
        else:
            logger.warning(f"Email connection test failed: {message}")
            return JsonResponse({
                'success': False,
                'error': message
            })
            
    except Exception as e:
        logger.error(f"Error testing email configuration: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error testing email: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def send_test_email_view(request):
    """Send test email"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        to_email = data.get('to_email', request.user.email)
        
        config = SystemConfig.objects.get(id=1)
        
        # Send test email
        success = send_test_email(to_email, config)
        
        if success:
            logger.info(f"Test email sent to {to_email} by {request.user.email}")
            return JsonResponse({
                'success': True,
                'message': f'Test email sent successfully to {to_email}'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Failed to send test email. Please check your configuration.'
            })
            
    except Exception as e:
        logger.error(f"Error sending test email: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error sending test email: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def test_sms_config(request):
    """Test SMS/Twilio configuration"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        config = SystemConfig.objects.get(id=1)
        
        # Test connection
        success, message = test_sms_connection(config)
        
        if success:
            logger.info(f"SMS connection test successful by {request.user.email}")
            return JsonResponse({
                'success': True,
                'message': message
            })
        else:
            logger.warning(f"SMS connection test failed: {message}")
            return JsonResponse({
                'success': False,
                'error': message
            })
            
    except Exception as e:
        logger.error(f"Error testing SMS configuration: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error testing SMS: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def send_test_sms_view(request):
    """Send test SMS"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        to_phone = data.get('to_phone')
        
        if not to_phone:
            return JsonResponse({
                'success': False,
                'error': 'Phone number is required'
            }, status=400)
        
        config = SystemConfig.objects.get(id=1)
        
        # Send test SMS
        success, message = send_test_sms(to_phone, config)
        
        if success:
            logger.info(f"Test SMS sent to {to_phone} by {request.user.email}")
            return JsonResponse({
                'success': True,
                'message': f'Test SMS sent successfully to {to_phone}'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': message
            })
            
    except Exception as e:
        logger.error(f"Error sending test SMS: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error sending test SMS: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@user_passes_test(is_system_admin)
def apply_email_preset(request):
    """Apply email preset configuration"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        provider = data.get('provider')
        
        if provider not in EMAIL_PRESETS:
            return JsonResponse({
                'success': False,
                'error': 'Invalid email provider'
            }, status=400)
        
        preset = EMAIL_PRESETS[provider]
        
        logger.info(f"Email preset '{provider}' applied by {request.user.email}")
        
        return JsonResponse({
            'success': True,
            'preset': preset
        })
        
    except Exception as e:
        logger.error(f"Error applying email preset: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error applying preset: {str(e)}'
        }, status=400)
