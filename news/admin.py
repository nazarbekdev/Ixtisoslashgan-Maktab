from django.contrib import admin
from .models import News, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'image', 'description', 'content', 'author', 'created_at', 'views']
    search_fields = ['title', 'category', 'author']
    