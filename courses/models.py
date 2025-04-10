from django.db import models
from accounts.models import CustomUser


class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Sinf'
        verbose_name_plural = 'Sinflar'


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'
        

class OfflineStudent(models.Model):
    count = models.IntegerField()
    
    def __str__(self):
        return str(self.count)
    
    class Meta:
        verbose_name = 'Oflayn Student'
        verbose_name_plural = 'Oflayn Studentlar'


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_subjects')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='student_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_subjects')
    reyting = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.student} - {self.subject}'

    class Meta:
        verbose_name = 'Talaba Fan'
        verbose_name_plural = 'Talaba Fanlari'
     

class TeacherExpertise(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_expertise')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='teacher_expertise')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_expertise')
    
    def __str__(self):
        return f'{self.teacher} - {self.subject}'

    class Meta:
        verbose_name = 'O\'qituvchi Mutahasislik'
        verbose_name_plural = 'O\'qituvchi Mutahasisliklari'
           

class TeacherCLass(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_subjects')
    class_number = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='teacher_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_subjects')
    
    def __str__(self):
        return f'{self.teacher} - {self.subject}'

    class Meta:
        verbose_name = 'O\'qituvchi Sinf'
        verbose_name_plural = 'O\'qituvchi Sinflari'
        

class Topic(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1, related_name='teacher_topics')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    video_url = models.URLField(blank=True, null=True, )
    lecture_file = models.FileField(upload_to='media/lectures/', blank=True, null=True)
    presentation_file = models.FileField(upload_to='media/presentations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Yuklangan material'
        verbose_name_plural = 'Yuklangan materiallar'
