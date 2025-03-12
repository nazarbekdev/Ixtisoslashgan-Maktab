from rest_framework import serializers
from .models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        