from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'email', 'role', 'region', 'school', 'class_id', 'gender', 'subject', 'image', 'district']
    
    def create(self, validated_data):
        # Parolni alohida olish va olib tashlash
        password = validated_data.pop('password')
        
        # Image maydonini alohida olish va olib tashlash
        image = validated_data.pop('image', None)
        
        user = CustomUser(
            username=validated_data.get('username'),
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role', 'student'),
            subject=validated_data.get('subject', ''),
            region=validated_data.get('region', ''),
            district=validated_data.get('district', ''),
            school=validated_data.get('school', ''),
            class_id=validated_data.get('class_id', ''),
            gender=validated_data.get('gender', '')
        )
        
        # Parolni o'rnatish
        user.set_password(password)
        
        # Foydalanuvchini saqlash
        user.save()
        
        # Agar rasm bo'lsa, uni saqlash
        if image:
            user.image.save(image.name, image, save=True)
        
        return user
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'subject', 'region', 'school']
        