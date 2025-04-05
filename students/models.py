from django.db import models
from accounts.models import CustomUser
from courses.models import Subject, Class
from tests.models import Variant


class TestType(models.Model):
    name = models.CharField(max_length=50)
    duration = models.IntegerField(default=60)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Test turi"
        verbose_name_plural = "Test turlari"


class Submission(models.Model):
    from teachers.models import Material
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/submissions/')
    grade = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.material.topic}"
    
    class Meta:
        verbose_name = "Student vazifa"
        verbose_name_plural = "Student vazifalar"


class TestResult(models.Model):
    QUARTER_CHOICES = [
        ('I chorak', 'I chorak'),
        ('II chorak', 'II chorak'),
        ('III chorak', 'III chorak'),
        ('IV chorak', 'IV chorak'),
    ]

    student = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('courses.Subject', on_delete=models.CASCADE, related_name='results')
    test_type = models.ForeignKey('TestType', on_delete=models.CASCADE, related_name='results')
    variant = models.ForeignKey('tests.Variant', on_delete=models.CASCADE, null=True, related_name='variant_results')
    quarter = models.CharField(max_length=20, choices=QUARTER_CHOICES, null=True, blank=True)
    correct = models.CharField(max_length=10)  # To‘g‘ri javoblar soni (masalan, "5/10")
    score = models.CharField(max_length=10)  # Umumiy ball (masalan, "15.0/20.0")
    percentage = models.FloatField(null=True, blank=True)  # Foiz (masalan, 75.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.test_type.name} - {self.subject.name}"

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalar"


class TestResultDetail(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='details')
    question = models.ForeignKey('tests.Question', on_delete=models.CASCADE, related_name='result_details')
    user_answer = models.TextField(null=True, blank=True)  # Foydalanuvchi javobi
    is_correct = models.BooleanField()  # To‘g‘ri yoki noto‘g‘ri
    score = models.FloatField()  # Savolning balli (agar to‘g‘ri bo‘lsa, savolning balli, aks holda 0)
    question_type = models.CharField(max_length=50)  # Savol turi (masalan, "yopiq" yoki "ochiq")
    difficulty = models.CharField(max_length=50)  # Savol darajasi (masalan, "Q", "M", "B")

    def __str__(self):
        return f"Detail for {self.test_result} - Question {self.question.id}"
