from django.contrib import admin
from .models import Class, Subject, OfflineStudent

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(OfflineStudent)
class OfflineStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'count']
    search_fields = ['count']
    