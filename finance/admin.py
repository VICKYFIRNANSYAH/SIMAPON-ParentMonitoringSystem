from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'month', 'year', 'amount', 'status', 'created_at')
    list_filter = ('status', 'year', 'month')
    search_fields = ('student__name', 'student__nis')
