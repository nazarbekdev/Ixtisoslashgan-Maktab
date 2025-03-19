from rest_framework import serializers
from .models import Submission, TestResult, TestType

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
        
class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
        