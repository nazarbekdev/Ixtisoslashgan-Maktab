from django.urls import path
from .views import ChatAPIView, ChatHistoryAPIView

urlpatterns = [
    path('api/chat/', ChatAPIView.as_view(), name='chat'),
    path('api/chat/history/', ChatHistoryAPIView.as_view(), name='chat-history'),
]