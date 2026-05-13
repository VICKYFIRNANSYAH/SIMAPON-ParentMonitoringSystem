from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_guru', 'is_parent', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('is_admin', 'is_guru', 'is_parent', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)
