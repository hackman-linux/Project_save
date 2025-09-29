from django.db import migrations, models
import uuid
from django.conf import settings

class Migration(migrations.Migration):

    initial = False  # important, not an initial migration
    dependencies = [
        ('notifications', '0001_initial'),  # or whatever your last applied migration is
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications', db_column='user_id')),
                ('notification', models.ForeignKey(to='notifications.Notification', on_delete=models.CASCADE, related_name='user_notifications', db_column='notification_id')),
            ],
            options={
                'db_table': 'notifications_usernotification',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'notification')},
            },
        ),
    ]
