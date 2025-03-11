from django.urls import path
from .views import CategoryListAPIView, NewsListAPIView, PopularNewsAPIView, NewsDetailAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('popular-news/', PopularNewsAPIView.as_view(), name='popular-news'),
    path('news/<int:pk>/', NewsDetailAPIView.as_view(), name='news-detail'),
]
