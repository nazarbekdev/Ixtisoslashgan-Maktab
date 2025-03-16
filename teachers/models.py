from django.db import models
from courses.models import Class, Subject

class Material(models.Model):

    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='materials')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    task_type = models.CharField(max_length=10, choices=(('Sinf', 'Sinf'), ('Kurs', 'Kurs')))
    topic = models.CharField(max_length=255)
    lecture_file = models.FileField(upload_to='media/lectures/', null=True, blank=True)
    presentation_file = models.FileField(upload_to='presentations/', null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"


class TestFile(models.Model):
    subject = models.CharField(max_length=50)
    class_number = models.CharField(max_length=50)
    topic = models.CharField(max_length=255)
    quanity = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/tests/', null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Test Fayl"
        verbose_name_plural = "Test Fayllar"