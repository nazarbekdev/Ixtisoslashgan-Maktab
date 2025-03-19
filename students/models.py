from django.db import models
from accounts.models import CustomUser
from teachers.models import Material
from courses.models import Subject, Class


class TestType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Test turi"
        verbose_name_plural = "Test turlari"


class Submission(models.Model):
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
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    correct = models.CharField(max_length=10)
    score = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name}"
    
    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalar"
        