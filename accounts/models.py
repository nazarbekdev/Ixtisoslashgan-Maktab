from django.contrib.auth.models import AbstractUser
from django.db import models
# from courses.models import Class

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'O‘qituvchi'),
        ('student', 'Talaba'),
    )
    GENDER_CHOICES = (
        ('Erkak', 'Erkak'),
        ('Ayol', 'Ayol'),
    )
    
    username = models.CharField(max_length=255, unique=True, help_text="Telefon raqam yoki Email")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='media/user_image/', null=True, blank=True, help_text="Profil rasmi")
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True, help_text="Telefon raqam")
    email = models.EmailField(blank=True, null=True, help_text="Ixtiyoriy")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    subject = models.CharField(max_length=100, blank=True, null=True, help_text="O‘qituvchi uchun fan yo‘nalishi")
    region = models.CharField(max_length=100, blank=True, null=True, help_text="Talaba uchun viloyat")
    district = models.CharField(max_length=100, blank=True, null=True, help_text="Talaba uchun tuman")
    school = models.CharField(max_length=100, blank=True, null=True, help_text="Talaba uchun maktab")
    class_id = models.ForeignKey('courses.Class', on_delete=models.CASCADE, null=True, blank=True, related_name='users', help_text="Talaba uchun sinf")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, help_text="Talaba uchun jins")

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        