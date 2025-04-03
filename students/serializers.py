from rest_framework import serializers
from .models import Submission, TestResult, TestType, TestResultDetail


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
        fields = ['question', 'user_answer', 'is_correct', 'score']


class TestResultSerializer(serializers.ModelSerializer):
    details = TestResultDetailSerializer(many=True, write_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'student', 'subject', 'test_type', 'variant', 'quarter', 'correct', 'score', 'percentage',
                  'is_active', 'created_at', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        test_result = TestResult.objects.create(**validated_data)

        # Har bir savol bo‘yicha natijani saqlash
        for detail_data in details_data:
            TestResultDetail.objects.create(test_result=test_result, **detail_data)

        return test_result
