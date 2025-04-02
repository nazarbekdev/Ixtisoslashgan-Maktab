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

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'correct_answer', 'option_1', 'option_2', 'option_3',
            'score', 'test_type', 'subject', 'variant', 'class_number',
            'question_type', 'difficulty', 'image', 'created_at'
        ]