from rest_framework import serializers
from .models import Variant, Question


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    test_type = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    variant = serializers.StringRelatedField()
    class_number = serializers.StringRelatedField()
    question_type = serializers.StringRelatedField()
    difficulty = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()  # image maydonini dinamik qaytarish uchun

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'correct_answer', 'option_1', 'option_2', 'option_3',
            'score', 'test_type', 'subject', 'variant', 'class_number',
            'question_type', 'difficulty', 'image', 'created_at'
        ]

    def get_image(self, obj):
        # Agar image mavjud bo‘lsa, to‘liq URL’ni qaytarish
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')  # Request kontekstini olish
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            # Agar request konteksti bo‘lmasa, default URL qaytarish
            return f"http://127.0.0.1:8000{obj.image.url}"
        return None  # Agar image bo‘lmasa, None qaytarish
