from django.contrib import admin
from .models import Submission, TestResult, TestType, TestResultDetail


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'class_number', 'subject', 'material', 'grade', 'file', 'submitted_at')
    list_filter = ('student', 'material', 'submitted_at')
    search_fields = ('student', 'material', 'submitted_at')


class TestResultDetailInline(admin.TabularInline):
    model = TestResultDetail
    extra = 0


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'test_type', 'correct', 'score', 'is_active', 'created_at')
    list_filter = ('student', 'subject', 'test_type', 'created_at', 'is_active')
    search_fields = ('student', 'subject', 'test_type', 'created_at')
    list_editable = ('is_active',)


@admin.register(TestResultDetail)
class TestResultDetailAdmin(admin.ModelAdmin):
    list_display = ('test_result', 'question', 'user_answer', 'is_correct', 'score')
    list_filter = ('is_correct',)


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration')
    list_filter = ('name',)
    search_fields = ('name',)
    list_editable = ('duration',)
