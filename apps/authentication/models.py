from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
import uuid

class User(AbstractUser):
    # Create your models here with role-based access.

    ROLE_CHOICE = [
        ('employee', 'Employee'),
        ('canteen_admin', 'Canteen Admin'),
        ('system_admin', 'System Admin'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    # Core fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Fixed: was default-uuid.uuid4
    email = models.EmailField(unique=True, db_index=True)
    phone_regex = RegexValidator(
        regex=r'^\+?237?[2368]\d{7,8}$',
        message="Phone number must be in Cameroon format: +237XXXXXXXXX"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        help_text="Cameroon phone number format"
    )

    # Profile fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='employee')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True
    )
    
    # Wallet and preferences
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preferred_payment_method = models.CharField(
        max_length=20, 
        choices=[
            ('wallet', 'Wallet'),
            ('mtn_momo', 'MTN Mobile Money'),
            ('orange_money', 'Orange Money'),
        ],  # Fixed: removed settings.CANTEEN_SETTINGS reference
        default='wallet'
    )
    
    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Authentication fields
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    
    # Activity tracking
    last_activity = models.DateTimeField(blank=True, null=True)
    login_count = models.PositiveIntegerField(default=0)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(blank=True, null=True)
    
    # Use email as the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
            models.Index(fields=['employee_id']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the short name of the user"""
        return self.first_name or self.username
    
    def get_role_display_color(self):
        """Return Bootstrap color class for user role"""
        role_colors = {
            'employee': 'primary',
            'canteen_admin': 'warning',
            'system_admin': 'danger'
        }
        return role_colors.get(self.role, 'secondary')
    
    def get_status_display_color(self):
        """Return Bootstrap color class for user status"""
        status_colors = {
            'active': 'success',
            'inactive': 'secondary',
            'suspended': 'danger'
        }
        return status_colors.get(self.status, 'secondary')
    
    def is_employee(self):
        """Check if user is an employee"""
        return self.role == 'employee'
    
    def is_canteen_admin(self):
        """Check if user is a canteen admin"""
        return self.role == 'canteen_admin'
    
    def is_system_admin(self):
        """Check if user is a system admin"""
        return self.role == 'system_admin' or self.is_superuser
    
    def can_place_orders(self):
        """Check if user can place orders"""
        return self.role == 'employee' and self.status == 'active'
    
    def can_manage_orders(self):
        """Check if user can manage orders"""
        return self.role in ['canteen_admin', 'system_admin'] and self.status == 'active'
    
    def can_manage_users(self):
        """Check if user can manage users"""
        return self.role == 'system_admin' and self.status == 'active'
    
    def add_to_wallet(self, amount):
        """Add amount to user's wallet"""
        self.wallet_balance += amount
        self.save(update_fields=['wallet_balance'])
        return self.wallet_balance
    
    def deduct_from_wallet(self, amount):
        """Deduct amount from user's wallet"""
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            self.save(update_fields=['wallet_balance'])
            return True
        return False
    
    def has_sufficient_balance(self, amount):
        """Check if user has sufficient wallet balance"""
        return self.wallet_balance >= amount
    
    def generate_employee_id(self):
        """Generate unique employee ID"""
        if not self.employee_id:
            year = self.date_joined.year if self.date_joined else 2024
            last_user = User.objects.filter(
                employee_id__startswith=f"EMP{year}"
            ).order_by('-employee_id').first()
            
            if last_user and last_user.employee_id:
                last_number = int(last_user.employee_id[7:])  # EMP2024001
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.employee_id = f"EMP{year}{new_number:03d}"
            self.save(update_fields=['employee_id'])
        
        return self.employee_id
    
    def update_last_activity(self):
        """Update user's last activity timestamp"""
        from django.utils import timezone
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    def increment_login_count(self):
        """Increment user's login count"""
        self.login_count += 1
        self.failed_login_attempts = 0  # Reset failed attempts on successful login
        self.save(update_fields=['login_count', 'failed_login_attempts'])
    
    def increment_failed_login(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            from django.utils import timezone
            from datetime import timedelta
            self.account_locked_until = timezone.now() + timedelta(minutes=30)
        
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    def is_account_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            from django.utils import timezone
            if timezone.now() < self.account_locked_until:
                return True
            else:
                # Unlock account
                self.account_locked_until = None
                self.failed_login_attempts = 0
                self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
        return False


class UserActivity(models.Model):
    """Track user activities for audit purposes"""
    
    ACTIVITY_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('order_placed', 'Order Placed'),
        ('payment_made', 'Payment Made'),
        ('profile_updated', 'Profile Updated'),
        ('password_changed', 'Password Changed'),
        ('admin_action', 'Admin Action'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='activities'
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional context data (JSON field for flexibility)
    extra_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'user_activity'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type} at {self.timestamp}"


class UserSession(models.Model):
    """Track active user sessions"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_session'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.user.email} - {self.session_key[:8]}..."
    
    def deactivate(self):
        """Deactivate the session"""
        self.is_active = False
        self.save(update_fields=['is_active'])

class SystemConfig(models.Model):
    """System-wide configuration for the application"""

    # General settings
    app_name = models.CharField(max_length=100, default="Canteen Management System")
    app_version = models.CharField(max_length=20, default="1.0.0")
    timezone = models.CharField(max_length=50, default="Africa/Douala")
    currency = models.CharField(max_length=10, default="XAF")
    language = models.CharField(max_length=10, default="en")

    # Business settings
    opening_time = models.TimeField(default="08:00")
    closing_time = models.TimeField(default="18:00")
    order_processing_time = models.IntegerField(default=15, help_text="Average time in minutes")
    max_daily_orders = models.IntegerField(default=200)
    cancellation_window = models.IntegerField(default=10, help_text="Minutes before order can be cancelled")
    allow_advance_orders = models.BooleanField(default=True)

    # Payment settings
    mtn_enabled = models.BooleanField(default=True)
    mtn_api_key = models.CharField(max_length=255, blank=True, null=True)
    mtn_merchant_id = models.CharField(max_length=100, blank=True, null=True)
    mtn_environment = models.CharField(max_length=20, default="sandbox")
    
    orange_enabled = models.BooleanField(default=False)
    orange_api_key = models.CharField(max_length=255, blank=True, null=True)
    orange_merchant_id = models.CharField(max_length=100, blank=True, null=True)
    orange_environment = models.CharField(max_length=20, default="sandbox")
    
    payment_timeout = models.IntegerField(default=120, help_text="Seconds")
    transaction_fee = models.DecimalField(max_digits=5, decimal_places=2, default=2.5)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    auto_refund = models.BooleanField(default=True)

    # Email notification settings
    email_enabled = models.BooleanField(default=True)
    smtp_server = models.CharField(max_length=100, default="smtp.gmail.com")
    smtp_port = models.IntegerField(default=587)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_use_ssl = models.BooleanField(default=False)
    from_email = models.EmailField(default="noreply@canteen.com")
    smtp_username = models.CharField(max_length=100, blank=True, null=True)
    smtp_password = models.CharField(max_length=255, blank=True, null=True)
    
    # SMS notification settings (Twilio)
    sms_enabled = models.BooleanField(default=False)
    sms_provider = models.CharField(max_length=50, default="twilio", choices=[
        ('twilio', 'Twilio'),
        ('nexmo', 'Nexmo/Vonage'),
        ('local', 'Local Provider')
    ])
    twilio_account_sid = models.CharField(max_length=255, blank=True, null=True)
    twilio_auth_token = models.CharField(max_length=255, blank=True, null=True)
    sms_from_number = models.CharField(max_length=20, blank=True, null=True, help_text="E.164 format: +237XXXXXXXXX")
    
    # Push notifications
    push_enabled = models.BooleanField(default=False)
    firebase_server_key = models.CharField(max_length=255, blank=True, null=True)

    # Notification preferences
    notify_order_placed = models.BooleanField(default=True)
    notify_order_ready = models.BooleanField(default=True)
    notify_payment_success = models.BooleanField(default=True)
    notify_order_cancelled = models.BooleanField(default=True)
    notify_low_balance = models.BooleanField(default=True)

    # Security settings
    session_timeout = models.IntegerField(default=60, help_text="Minutes")
    password_min_length = models.IntegerField(default=8)
    require_uppercase = models.BooleanField(default=True)
    require_numbers = models.BooleanField(default=True)
    require_special_chars = models.BooleanField(default=False)
    max_login_attempts = models.IntegerField(default=5)
    lockout_duration = models.IntegerField(default=15, help_text="Minutes")
    enable_2fa = models.BooleanField(default=False)
    log_security_events = models.BooleanField(default=True)
    require_password_change = models.BooleanField(default=False)

    # Maintenance settings
    auto_backup = models.BooleanField(default=True)
    backup_frequency = models.CharField(max_length=20, default="daily", choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ])
    backup_time = models.TimeField(default="02:00")
    backup_retention = models.IntegerField(default=30, help_text="Days")
    
    performance_monitoring = models.BooleanField(default=True)
    log_level = models.CharField(max_length=20, default="INFO", choices=[
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error')
    ])
    log_retention = models.IntegerField(default=30, help_text="Days")
    email_alerts = models.BooleanField(default=True)
    
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(
        default="System under maintenance, please check back later."
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"
        db_table = "system_config"

    def __str__(self):
        return f"SystemConfig (Last updated: {self.updated_at})"

    def get_smtp_settings(self):
        """Get SMTP settings as dictionary"""
        return {
            'server': self.smtp_server,
            'port': self.smtp_port,
            'use_tls': self.smtp_use_tls,
            'use_ssl': self.smtp_use_ssl,
            'username': self.smtp_username,
            'password': self.smtp_password,
            'from_email': self.from_email,
        }

    def get_twilio_settings(self):
        """Get Twilio settings as dictionary"""
        return {
            'account_sid': self.twilio_account_sid,
            'auth_token': self.twilio_auth_token,
            'from_number': self.sms_from_number,
        }

    def is_email_configured(self):
        """Check if email is properly configured"""
        return all([
            self.email_enabled,
            self.smtp_server,
            self.smtp_port,
            self.smtp_username,
            self.smtp_password,
            self.from_email
        ])

    def is_sms_configured(self):
        """Check if SMS is properly configured"""
        if self.sms_provider == 'twilio':
            return all([
                self.sms_enabled,
                self.twilio_account_sid,
                self.twilio_auth_token,
                self.sms_from_number
            ])
        return False

    def is_push_configured(self):
        """Check if push notifications are configured"""
        return self.push_enabled and self.firebase_server_key
