from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from accounts.serializers import RegisterSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class StudentProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)
            serializer = RegisterSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)
            serializer = RegisterSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StudentProfileImageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)
            if 'image' in request.FILES:
                image = request.FILES['image']
                if user.image:
                    user.image.delete()  # Eski rasmni o'chirish
                user.image.save(image.name, ContentFile(image.read()))
                user.save()
                serializer = RegisterSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Rasm yuborilmadi'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)