from django.db import models


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


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    video_url = models.URLField(blank=True, null=True, )
    lecture_file = models.FileField(upload_to='lectures/', blank=True, null=True)
    presentation_file = models.FileField(upload_to='presentations/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mavzu'
        verbose_name_plural = 'Mavzular'


# o'zgaradi...
class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='tests')
    class_level = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=100)
    questions = models.JSONField()  # Hozircha savollar JSON formatida saqlanadi, ammo alohida model qilinadi (TestQuestion modeli)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'
    