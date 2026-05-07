from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nis', 'name', 'grade', 'parent')
    search_fields = ('nis', 'name', 'parent__username')
    list_filter = ('grade',)
