from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Pesantren Profile', {'fields': ('role', 'siswa_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Pesantren Profile', {'fields': ('role', 'siswa_id')}),
    )
    list_display = ('username', 'email', 'role', 'siswa_id', 'is_staff')

admin.site.register(User, CustomUserAdmin)
