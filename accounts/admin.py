from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role', 'phone_number', 'email', 'first_name', 'last_name', 'subject', 'region', 'school', 'class_id', 'gender']
    list_filter = ['role', 'gender']
    search_fields = ['username', 'phone_number', 'email']
    