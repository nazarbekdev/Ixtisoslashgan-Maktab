from django.db import models
from django.core.validators import RegexValidator

class ContactRequest(models.Model):
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+998[0-9]{9}$', message="Telefon raqami +998 bilan boshlanib, 9 ta raqamdan iborat bo'lishi kerak.")]
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        verbose_name = 'Murojaat'
        verbose_name_plural = 'Murojaatlar'
        