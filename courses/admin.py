from django.contrib import admin
from .models import Class, Subject, OfflineStudent, Topic, StudentSubject, TeacherCLass, TeacherExpertise


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
    list_display = ['id', 'teacher', 'title', 'video_url', 'lecture_file', 'presentation_file', 'subject',
                    'class_level']


@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'subject', 'class_number', 'reyting']
    search_fields = ['student', 'subject', 'class_number']


@admin.register(TeacherCLass)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'class_number', 'subject']
    search_fields = ['teacher', 'class_number', 'subject']


@admin.register(TeacherExpertise)
class TeacherExpertiseAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'class_number', 'subject']
    search_fields = ['teacher', 'class_number', 'subject']
