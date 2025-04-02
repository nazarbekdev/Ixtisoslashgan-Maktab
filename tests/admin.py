from django.contrib import admin

from .models import Question, QuestionType, TestFile, TestControl, Variant, QuestionDifficulty


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_type', 'class_number', 'subject', 'text', 'correct_answer', 'difficulty','created_at')
    list_filter = ('class_number', 'subject', 'variant')
    search_fields = ('text',)


@admin.register(TestFile)
class TestFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'file')


@admin.register(TestControl)
class TestControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'test_type', 'question_type', 'limit')


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(QuestionDifficulty)
class QuestionDifficultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
