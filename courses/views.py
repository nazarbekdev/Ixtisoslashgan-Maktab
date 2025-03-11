from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Class, Subject, OfflineStudent, Topic, Test
from .serializers import ClassSerializer, SubjectSerializer, OfflineStudentSerializer, TopicSerializer, TestSerializer

# Class uchun API
class ClassListCreateAPIView(GenericAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha Class'larni ro'yxat qilish
        classes = self.get_queryset()
        serializer = self.get_serializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi Class yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Subject uchun API
class SubjectListCreateAPIView(GenericAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha Subject'larni ro'yxat qilish
        subjects = self.get_queryset()
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi Subject yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OfflineStudentAPIView(GenericAPIView):
    queryset = OfflineStudent.objects.all()
    serializer_class = OfflineStudentSerializer

    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha OfflineStudent'larni ro'yxat qilish
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi OfflineStudent yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TopicListAPIView(ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        class_id = self.request.query_params.get('class_id')
        return Topic.objects.filter(subject_id=subject_id, class_level_id=class_id)

# o'zgaradi...
class TestListAPIView(ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        class_id = self.request.query_params.get('class_id')
        return Test.objects.filter(subject_id=subject_id, class_level_id=class_id)
