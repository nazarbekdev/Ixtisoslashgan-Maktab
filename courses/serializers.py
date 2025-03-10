from rest_framework import serializers
from .models import Class, Subject, OfflineStudent

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class OfflineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineStudent
        fields = '__all__'
        