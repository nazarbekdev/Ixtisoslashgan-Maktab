# views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, AllUserSerializer
from .models import CustomUser
import uuid
import requests

# Telegram bot tokeni va chat ID (sozlamalarda saqlanadi)
TELEGRAM_BOT_TOKEN = "7770078413:AAG51717kVpS-0P_-s3yqTvEfKsz_b2WUl8"  # Telegram bot tokeningizni kiriting
TELEGRAM_BOT_URL = f"https://t.me/ai_edu_reset_password_bot"  # Botning URL manzili


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUserAPIView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetRequestAPIView(GenericAPIView):
    permission_classes = ()

    """
    Foydalanuvchi telefon raqamini kiritadi va Telegram bot orqali parol tiklash jarayonini boshlaydi.
    """

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        try:
            user = CustomUser.objects.get(username=phone_number)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Bu telefon raqami bilan foydalanuvchi topilmadi.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Vaqtinchalik token generatsiya qilish
        token = str(uuid.uuid4())
        user.password_reset_token = token
        user.save()

        # Telegram bot linkini qaytarish
        telegram_link = f"{TELEGRAM_BOT_URL}?start={token}"
        return Response({
            'message': 'Telegram bot orqali parolni tiklash uchun quyidagi linkka o‘ting.',
            'telegram_link': telegram_link,
            'token': token  # Tokenni frontendda ko‘rsatish uchun
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(GenericAPIView):
    permission_classes = ()

    """
    Telegram bot orqali yangi parolni tasdiqlash va o‘rnatish.
    """

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            user = CustomUser.objects.get(password_reset_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Noto‘g‘ri token yoki foydalanuvchi topilmadi.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Yangi parolni o‘rnatish
        user.set_password(new_password)
        user.password_reset_token = None  # Tokenni o‘chirish
        user.save()

        return Response({'message': 'Parol muvaffaqiyatli yangilandi.'}, status=status.HTTP_200_OK)
