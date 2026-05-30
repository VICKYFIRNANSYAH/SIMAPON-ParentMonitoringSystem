from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Notification

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_guru', 'is_parent', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('is_admin', 'is_guru', 'is_parent', 'phone_number')}),
    )

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Notification, NotificationAdmin)
