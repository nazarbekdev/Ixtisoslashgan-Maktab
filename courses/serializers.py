from rest_framework import serializers
from .models import Class, Subject, OfflineStudent, Topic, StudentSubject, TeacherCLass, TeacherExpertise

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
        
class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = '__all__'


class TeacherExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherExpertise
        fields = '__all__'
        

class TeacherClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCLass
        fields = '__all__'
        
class OfflineStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineStudent
        fields = '__all__'
        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'video_url', 'lecture_file', 'presentation_file']
        

        