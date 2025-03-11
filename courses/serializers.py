from rest_framework import serializers
from .models import Class, Subject, OfflineStudent, Topic, Test

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
        
class OfflineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineStudent
        fields = '__all__'
        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'video_url', 'lecture_file', 'presentation_file']
        
# o'zgaradi...
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title', 'questions']
        