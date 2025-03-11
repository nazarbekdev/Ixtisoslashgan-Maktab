from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        

class News(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    description = models.TextField()  # Qisqacha tavsif
    content = models.TextField()  # To'liq matn (batafsil uchun)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)  # Mashhurlikni aniqlash uchun ko'rishlar soni

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        