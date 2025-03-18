from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Material
from .serializers import MaterialSerializer, TeacherSerializer


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
        