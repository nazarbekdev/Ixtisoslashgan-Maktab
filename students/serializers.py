from rest_framework import serializers
from .models import Submission, TestResult, TestType, TestResultDetail, Feedback


class SubmissionSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'file', 'submitted_at', 'student', 'material', 'class_number', 'subject', 'grade']

    def get_file(self, obj):
        # Faylning to‘liq URL ini qaytarish
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = '__all__'


class TestResultDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResultDetail
        fields = ['question', 'user_answer', 'is_correct', 'score', 'question_type', 'difficulty']


class TestResultSerializer(serializers.ModelSerializer):
    details = TestResultDetailSerializer(many=True, write_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'student', 'subject', 'test_type', 'variant', 'quarter', 'correct', 'score', 'percentage',
                  'is_active', 'created_at', 'details']

    def create(self, validated_data):
        # `details` ma'lumotlarini olish va olib tashlash
        details_data = validated_data.pop('details', [])
        # TestResult obyektini yaratish
        test_result = TestResult.objects.create(**validated_data)

        # Har bir savol bo‘yicha natijani saqlash
        for detail_data in details_data:
            TestResultDetail.objects.create(test_result=test_result, **detail_data)

        return test_result

    def update(self, instance, validated_data):
        # `details` ma'lumotlarini olish va olib tashlash
        details_data = validated_data.pop('details', [])

        # TestResult obyektini yangilash
        instance.student = validated_data.get('student', instance.student)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.test_type = validated_data.get('test_type', instance.test_type)
        instance.variant = validated_data.get('variant', instance.variant)
        instance.quarter = validated_data.get('quarter', instance.quarter)
        instance.correct = validated_data.get('correct', instance.correct)
        instance.score = validated_data.get('score', instance.score)
        instance.percentage = validated_data.get('percentage', instance.percentage)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # Eski `TestResultDetail` larni o‘chirish (agar yangilash kerak bo‘lsa)
        instance.details.all().delete()

        # Yangi `TestResultDetail` larni qo‘shish
        for detail_data in details_data:
            TestResultDetail.objects.create(test_result=instance, **detail_data)

        return instance


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'student', 'question_id', 'question_text', 'user_answer', 'correct_answer', 'feedback_text',
                  'created_at']
