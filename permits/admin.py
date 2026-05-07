from django.contrib import admin
from .models import Permit

@admin.register(Permit)
class PermitAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date')
    search_fields = ('student__name', 'student__nis')
