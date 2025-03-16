from django.contrib import admin
from .models import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_number', 'subject', 'task_type', 'topic', 'deadline', 'created_at']
    list_filter = ['class_number', 'subject', 'task_type', 'deadline']
    search_fields = ['class_number', 'subject', 'task_type', 'topic']
