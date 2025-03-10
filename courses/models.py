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
        