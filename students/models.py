from django.db import models
from accounts.models import CustomUser
from teachers.models import Material

class Submission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.material.topic}"
    
    class Meta:
        verbose_name = "Student vazifa"
        verbose_name_plural = "Student vazifalar"
