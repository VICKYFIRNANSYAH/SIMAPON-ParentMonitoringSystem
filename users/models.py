from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_guru = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    
    # Phone number for contact
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
