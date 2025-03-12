from django.contrib import admin
from .models import ContactRequest

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    list_filter = ['created_at']
