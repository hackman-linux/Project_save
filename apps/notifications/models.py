from django.db import models
from django.conf import settings
from django.utils import timezone
from .fields import BinaryUUIDField
from apps.orders.models import Order

# ------------------------------------
# Shared constants
# ------------------------------------
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


# ------------------------------------
# Models
# ------------------------------------
class Notification(models.Model):
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_column='target_user_id'  # Explicitly specify the column name
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='order_id'  # Explicitly specify the column name
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_notifications",
        db_column='created_by_id'  # Explicitly specify the column name
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
        db_table = 'notifications_notification'  # Keep existing table name

    def __str__(self):
        return f"{self.title} → {self.target_user}"


class NotificationTemplate(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Template: {self.title} ({self.notification_type})"

    class Meta:
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"
        ordering = ["-created_at"]