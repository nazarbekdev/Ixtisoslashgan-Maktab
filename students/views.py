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
            serializer = RegisterSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)

            # Validatsiya uchun regions.json faylidan ro'yxatni o'qish
            import json
            with open('regions.json', 'r') as f:  # regions.json fayl yo'lini moslashtiring
                regions_data = json.load(f)
                valid_regions = [region['name'] for region in regions_data['regions']]
                valid_districts = []
                for region in regions_data['regions']:
                    valid_districts.extend(region['districts'])

            # region va district ni validatsiya qilish
            if 'region' in request.data and request.data['region'] and request.data['region'] not in valid_regions:
                return Response({'error': 'Noto‘g‘ri viloyat'}, status=status.HTTP_400_BAD_REQUEST)
            if 'district' in request.data and request.data['district'] and request.data['district'] not in valid_districts:
                return Response({'error': 'Noto‘g‘ri tuman'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RegisterSerializer(user, data=request.data, partial=True, context={'request': request})
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

            if 'image' not in request.FILES:
                return Response({'error': 'Rasm yuklanmadi'}, status=status.HTTP_400_BAD_REQUEST)

            image_file = request.FILES['image']
            if user.image and default_storage.exists(user.image.name):
                default_storage.delete(user.image.name)
            user.image = image_file
            user.save()

            serializer = RegisterSerializer(user, context={'request': request})
            return Response({'image': serializer.data['image']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)