from django.contrib import admin
from .models import BehaviorNote

@admin.register(BehaviorNote)
class BehaviorNoteAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'points', 'date')
    list_filter = ('category', 'date')
    search_fields = ('student__name', 'student__nis')
