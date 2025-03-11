from rest_framework import serializers
from .models import Category, News

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.ImageField(allow_null=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'category', 'image', 'description', 'content', 'author', 'created_at', 'views']
        