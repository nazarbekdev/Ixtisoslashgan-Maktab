from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Material, Test
from .serializers import MaterialSerializer, TeacherSerializer, MaterialNameSerializer, TestSerializer


# O‘qituvchi profilini olish va o‘zgartirish
class TeacherProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get(self, request):
        try:
            user = request.user
            if user.role != 'teacher':
                return Response({'error': 'Faqat o‘qituvchilar uchun'}, status=status.HTTP_403_FORBIDDEN)
            serializer = TeacherSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = request.user
            if user.role != 'teacher':
                return Response({'error': 'Faqat o‘qituvchilar uchun'}, status=status.HTTP_403_FORBIDDEN)

            serializer = TeacherSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Materiallarni ro‘yxatlash va yangi material qo‘shish uchun


class MaterialListCreateView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        # Barcha materiallarni olish
        materials = self.get_queryset()
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Yangi material qo‘shish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Bitta materialni olish uchun
class MaterialDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, pk, *args, **kwargs):
        # Bitta materialni ID bo‘yicha olish
        try:
            material = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(material)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Bitta material nomini olish uchun
class MaterialNameDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialNameSerializer

    def get(self, request, material_id, *args, **kwargs):
        try:
            material = self.get_queryset().get(id=material_id)
            serializer = self.get_serializer(material, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Teacher materiallarini olish uchun
class MaterialTeacherDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, teacher_id, *args, **kwargs):
        try:
            material = self.get_queryset().filter(teacher=teacher_id)
            serializer = self.get_serializer(material, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Fan va sinf uchun materiallar ro'yxatini olish
class MaterialByClassSubjectView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, class_id, subject_id, *args, **kwargs):
        try:
            material = self.get_queryset().filter(class_number=class_id, subject=subject_id)
            serializer = self.get_serializer(material, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Test yuklash
class TestUploadView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            # O‘qituvchi faqat o‘z testlarini yuklashi uchun
            if request.user.id != int(request.data.get('teacher')):
                return Response({'error': 'Siz faqat o‘zingizning testlaringizni yuklashingiz mumkin'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = TestSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Teacher ga tegishli testlarni olish
class TestListView(APIView):
    permission_classes = []

    def get(self, request, teacher_id, *args, **kwargs):
        try:
            tests = Test.objects.filter(teacher=teacher_id)
            serializer = TestSerializer(tests, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
