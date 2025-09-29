from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone
from apps.orders.models import Order

User = settings.AUTH_USER_MODEL

NOTIFICATION_TYPE_CHOICES = [
    ("order_status", "Order Status Update"),
    ("order_ready", "Order Ready"),
    ("order_cancelled", "Order Cancelled"),
    ("payment_success", "Payment Successful"),
    ("payment_failed", "Payment Failed"),
    ("menu_update", "Menu Update"),
    ("system_announcement", "System Announcement"),
    ("low_stock", "Low Stock Alert"),
    ("wallet_topup", "Wallet Top-up"),
    ("promotion", "Promotion/Offer"),
    ("maintenance", "System Maintenance"),
]


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_column="target_user_id",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="order_id",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_notifications",
        db_column="created_by_id",
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, default="system")
    priority = models.CharField(max_length=20, default="normal")
    action_url = models.CharField(max_length=255, blank=True)
    action_text = models.CharField(max_length=100, blank=True)
    target_audience = models.CharField(max_length=50, default="all")
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "notifications_notification"

    def __str__(self):
        return f"{self.title} → {self.target_user}"


class UserNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_notifications",
        db_column="user_id"  # Match your database column name
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="user_notifications",
        db_column="notification_id"  # Match your database column name
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ Changed from auto_now_add

    class Meta:
        db_table = 'notifications_usernotification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.notification.title}"


class NotificationTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications_template"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Template: {self.title} ({self.notification_type})"
