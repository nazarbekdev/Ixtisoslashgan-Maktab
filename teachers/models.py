from django.db import models
from accounts.models import CustomUser
from courses.models import Class, Subject


class Material(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='material_teacher')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='materials')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    task_type = models.CharField(max_length=10, choices=(('Sinf', 'Sinf'), ('Kurs', 'Kurs')))
    topic = models.CharField(max_length=255)
    lecture_file = models.FileField(upload_to='lectures/', null=True, blank=True)
    presentation_file = models.FileField(upload_to='presentations/', null=True, blank=True)
    test_file = models.FileField(upload_to='test/', null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"


class Test(models.Model):
    QUARTER_CHOICES = [
        ('I chorak', 'I chorak'),
        ('II chorak', 'II chorak'),
        ('III chorak', 'III chorak'),
        ('IV chorak', 'IV chorak'),
    ]

    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='tests')
    test_type = models.ForeignKey('students.TestType', on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='tests')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, related_name='tests')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    quarter = models.CharField(max_length=20, choices=QUARTER_CHOICES, null=True, blank=True)
    test_file = models.FileField(upload_to='tests/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.class_number} - {self.subject}"
