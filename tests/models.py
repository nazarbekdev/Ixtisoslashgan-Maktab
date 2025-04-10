from django.db import models
from courses.models import Class, Subject
from teachers.models import Material


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


class QuestionDifficulty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Savol darajasi'
        verbose_name_plural = 'Savol darajalari'


class Variant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variantlar'


class Question(models.Model):
    QUARTER_CHOICES = [
        ('I chorak', 'I chorak'),
        ('II chorak', 'II chorak'),
        ('III chorak', 'III chorak'),
        ('IV chorak', 'IV chorak'),
    ]

    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    quarter = models.CharField(max_length=20, choices=QUARTER_CHOICES, null=True, blank=True)
    test_type = models.ForeignKey('students.TestType', on_delete=models.CASCADE, default=1, related_name='questions')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.TextField()
    option_1 = models.TextField(null=True, blank=True)
    option_2 = models.TextField(null=True, blank=True)
    option_3 = models.TextField(null=True, blank=True)
    score = models.FloatField()
    difficulty = models.ForeignKey(QuestionDifficulty, on_delete=models.CASCADE, default=1, related_name='questions')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=1, related_name='questions')
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        indexes = [
                    models.Index(fields=['test_type', 'subject', 'variant', 'question_type', 'class_number', 'quarter']),
                ]


class TestControl(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_type = models.ForeignKey('students.TestType', on_delete=models.CASCADE, default=1)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, default=1)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=1)
    difficulty = models.ForeignKey(QuestionDifficulty, on_delete=models.CASCADE, default=1)
    limit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = 'Test Kontrol'
        verbose_name_plural = 'Test Kontrol'
        indexes = [
            models.Index(fields=['subject', 'test_type', 'variant']),
        ]
