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
        fields = '__all__'

        
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
    class Meta:
        model = Test
        fields = ['id', 'teacher', 'test_type', 'class_number', 'subject', 'topic', 'quarter', 'test_file', 'created_at']

    def validate(self, data):
        test_type = data.get('test_type')
        class_number = data.get('class_number')
        quarter = data.get('quarter')

        # Test turi "Fanga oid" bo‘lsa, class_number va quarter majburiy
        if test_type.name == 'Fanga oid':
            if not class_number:
                raise serializers.ValidationError("Fanga oid testlar uchun sinf tanlash majburiy!")
            if not quarter:
                raise serializers.ValidationError("Fanga oid testlar uchun chorak tanlash majburiy!")
        return data
