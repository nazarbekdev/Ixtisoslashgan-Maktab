from rest_framework import serializers
from .models import Material
from accounts.models import CustomUser


class MaterialSerializer(serializers.ModelSerializer):
    lecture_file = serializers.FileField(required=False, allow_null=True)
    presentation_file = serializers.FileField(required=False, allow_null=True)
    video_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Material
        fields = ['id', 'class_number', 'subject', 'task_type', 'topic', 'lecture_file', 'presentation_file', 'video_link', 'deadline', 'created_at']
        
        
class TeacherSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'image', 'phone_number', 'role']
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'image' in validated_data:
            instance.image = validated_data['image']
        instance.save()
        return instance