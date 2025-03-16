from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    lecture_file = serializers.FileField(required=False, allow_null=True)
    presentation_file = serializers.FileField(required=False, allow_null=True)
    video_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Material
        fields = ['id', 'class_number', 'subject', 'task_type', 'topic', 'lecture_file', 'presentation_file', 'video_link', 'deadline', 'created_at']