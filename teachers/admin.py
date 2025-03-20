from django.contrib import admin
from .models import Material, Test


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'class_number', 'subject', 'task_type', 'topic', 'deadline', 'created_at']
    list_filter = ['class_number', 'teacher', 'subject', 'task_type', 'deadline']
    search_fields = ['class_number', 'subject', 'task_type', 'topic']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'class_number', 'subject', 'topic', 'quarter', 'created_at']
    search_fields = ['class_number', 'subject', 'topic']