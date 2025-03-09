# auth/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'O‘qituvchi'),
        ('student', 'Talaba'),
    )
    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    )
    
    REGION_CHOICES = (
        ('qoraqalpogiston', "Qoraqalpog'iston Respublikasi"),
        ('andijon', 'Andijon viloyati'),
        ('buxoro', 'Buxoro viloyati'),
        ('jizzax', 'Jizzax viloyati'),
        ('qashqadaryo', "Qashqadaryo viloyati"),
        ('navoiy', 'Navoiy viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('samarkand', 'Samarkand viloyati'),
        ('surxondaryo', "Surxondaryo viloyati"),
        ('sirdaryo', 'Sirdaryo viloyati'),
        ('toshkent', 'Toshkent viloyati'),
        ('fargona', 'Farg‘ona viloyati'),
        ('xorazm', 'Xorazm viloyati'),
    )
    
    username = models.CharField(max_length=255, unique=True, help_text="Telefon raqam yoki Email")
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True, help_text="Telefon raqam")
    email = models.EmailField(blank=True, null=True, help_text="Ixtiyoriy")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    subject = models.CharField(max_length=100, blank=True, null=True, help_text="O‘qituvchi uchun fan yo‘nalishi")
    region = models.CharField(max_length=100, choices=REGION_CHOICES, blank=True, null=True, help_text="Talaba uchun viloyat")
    school = models.CharField(max_length=100, blank=True, null=True, help_text="Talaba uchun maktab")
    class_id = models.CharField(max_length=10, blank=True, null=True, help_text="Talaba uchun sinf")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, help_text="Talaba uchun jins")

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        