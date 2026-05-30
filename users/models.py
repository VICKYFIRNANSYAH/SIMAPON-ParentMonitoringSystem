import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def get_profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"profile_{instance.username}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('profiles/', new_filename)

class User(AbstractUser):
    # Multiple admin users can be created by setting is_admin=True
    is_admin = models.BooleanField(default=False)
    is_guru = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    
    # Phone number for contact
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # User profile picture
    profile_picture = models.ImageField(upload_to=get_profile_upload_path, blank=True, null=True, verbose_name="Foto Profil")

    class Meta:
        db_table = 'simapon_user'

    def __str__(self):
        return self.username


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('perizinan', 'Perizinan'),
        ('keuangan', 'Keuangan'),
        ('perilaku', 'Catatan Perilaku'),
        ('umum', 'Info Umum'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='umum')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'simapon_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"



