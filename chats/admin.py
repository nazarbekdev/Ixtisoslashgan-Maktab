from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'reply', 'timestamp']
    list_filter = ['timestamp', 'user']
    search_fields = ['message']
