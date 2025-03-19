from django.contrib import admin
from .models import Submission, TestResult, TestType


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'class_number', 'subject', 'material', 'grade', 'file', 'submitted_at')
    list_filter = ('student', 'material', 'submitted_at')
    search_fields = ('student', 'material', 'submitted_at')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'test_type', 'correct', 'score', 'created_at')
    list_filter = ('student', 'subject', 'test_type', 'created_at')
    search_fields = ('student', 'subject', 'test_type', 'created_at')

@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    