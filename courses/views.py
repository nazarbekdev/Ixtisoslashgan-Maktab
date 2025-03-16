from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Class, Subject, OfflineStudent, Topic, Test, StudentSubject, TeacherCLass, TeacherExpertise
from .serializers import ClassSerializer, SubjectSerializer, OfflineStudentSerializer, TopicSerializer, TestSerializer, StudentSubjectSerializer, TeacherClassSerializer, TeacherExpertiseSerializer

# Class uchun API
class ClassListCreateAPIView(GenericAPIView):
    permission_classes = []
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
    permission_classes = []
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request, *args, **kwargs):
        subjects = self.get_queryset()
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Topic uchun API
class TopicListAPIView(ListAPIView):
    permission_classes = []  
    serializer_class = TopicSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        class_id = self.request.query_params.get('class_id')
        return Topic.objects.filter(subject_id=subject_id, class_level_id=class_id)

# o'zgaradi...
class TestListAPIView(ListAPIView):
    permission_classes = []  
    serializer_class = TestSerializer

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id')
        class_id = self.request.query_params.get('class_id')
        return Test.objects.filter(subject_id=subject_id, class_level_id=class_id)

# OfflineStudent uchun API
class OfflineStudentAPIView(GenericAPIView):
    queryset = OfflineStudent.objects.all()
    serializer_class = OfflineStudentSerializer
    permission_classes = []
    
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
    
class StudentSubjectAPIView(GenericAPIView):
    queryset = StudentSubject.objects.all()
    serializer_class = StudentSubjectSerializer
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha StudentSubject'larni ro'yxat qilish
        students = self.get_queryset()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi StudentSubject yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bitta student ma'lumotini olish uchun
class StudentSubjectDetailView(GenericAPIView):
    queryset = StudentSubject.objects.all()
    serializer_class = StudentSubjectSerializer

    def get(self, request, student_id, *args, **kwargs):
        # Bitta materialni ID bo‘yicha olish
        try:
            subject = self.get_queryset().filter(student=student_id)
            serializer = self.get_serializer(subject, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentSubject.DoesNotExist:
            return Response({"error": "Student subject topilmadi"}, status=status.HTTP_404_NOT_FOUND)

class TeacherClassAPIView(GenericAPIView):
    queryset = TeacherCLass.objects.all()
    serializer_class = TeacherClassSerializer
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha TeacherSubject'larni ro'yxat qilish
        teachers = self.get_queryset()
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi TeacherSubject yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherExpertiseAPIView(GenericAPIView):
    queryset = TeacherExpertise.objects.all()
    serializer_class = TeacherExpertiseSerializer
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        # GET so'rov - barcha TeacherExpertise'larni ro'yxat qilish
        teachers = self.get_queryset()
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi TeacherExpertise yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherExpertiseDetailView(GenericAPIView):
    queryset = TeacherExpertise.objects.all()
    serializer_class = TeacherExpertiseSerializer

    def get(self, request, teacher_id, *args, **kwargs):
        # Bitta materialni ID bo‘yicha olish
        try:
            subject = self.get_queryset().filter(teacher=teacher_id)
            serializer = self.get_serializer(subject, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TeacherExpertise.DoesNotExist:
            return Response({"error": "Teacher expertise topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        