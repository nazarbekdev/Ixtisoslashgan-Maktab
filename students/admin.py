from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'material', 'file', 'submitted_at')
    list_filter = ('student', 'material', 'submitted_at')
    search_fields = ('student', 'material', 'submitted_at')
    list_per_page = 25
