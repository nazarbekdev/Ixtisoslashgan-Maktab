from django.contrib import admin
from .models import Class, Subject, OfflineStudent, Topic, Test

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
    
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_url', 'lecture_file', 'presentation_file', 'subject', 'class_level']
    
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'questions', 'subject', 'class_level']
    