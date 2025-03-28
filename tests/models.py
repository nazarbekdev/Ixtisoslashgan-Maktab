from django.db import models
from courses.models import Class, Subject
from students.models import TestType


class TestFile(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = 'Test Fayl'
        verbose_name_plural = 'Test Fayllar'


class QuestionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Savol turi'
        verbose_name_plural = 'Savol turi'


class Variant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variant'


class Question(models.Model):
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='questions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE, default=1, related_name='questions')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='questions', default=1)
    text = models.TextField()
    correct_answer = models.TextField()
    option_1 = models.TextField(null=True, blank=True)
    option_2 = models.TextField(null=True, blank=True)
    option_3 = models.TextField(null=True, blank=True)
    score = models.FloatField()
    difficulty = models.CharField(max_length=20)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=1, related_name='questions')
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"


class TestControl(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE, default=1)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, default=1)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=1)
    limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = 'Test Kontrol'
        verbose_name_plural = 'Test Kontrol'
