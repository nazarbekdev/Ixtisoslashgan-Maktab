from rest_framework import serializers
from .models import Material, Test
from accounts.models import CustomUser
from courses.models import Class, Subject


class MaterialSerializer(serializers.ModelSerializer):
    lecture_file = serializers.FileField(required=False, allow_null=True)
    presentation_file = serializers.FileField(required=False, allow_null=True)
    video_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Material
        fields = ['id', 'teacher', 'class_number', 'subject', 'task_type', 'topic', 'lecture_file', 'presentation_file', 'video_link', 'deadline', 'created_at']
  
        
class MaterialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'topic', 'deadline']
        
             
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


class TestSerializer(serializers.ModelSerializer):
    class_number = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    test_file = serializers.FileField()

    class Meta:
        model = Test
        fields = ['id', 'teacher', 'class_number', 'subject', 'topic', 'quarter', 'test_file', 'created_at']

    def to_representation(self, instance):
        # Fayl URL’ini qaytarish uchun
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.test_file and request:
            representation['test_file'] = request.build_absolute_uri(instance.test_file.url)
        else:
            representation['test_file'] = None
        return representation
