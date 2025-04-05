from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, AllUserSerializer
from .models import CustomUser


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = () 

    def post(self, request, *args, **kwargs):
        """
        Register a new user (Teacher or Student).

        POST request with the following parameters:
        - username (string): Phone number or email (required)
        - password (string): User password (required)
        - email (string): Optional email
        - first_name (string): User first name
        - last_name (string): User last name
        - phone_number (string): User phone number
        - role (string): 'teacher' or 'student' (required)
        - subject (string): Teacher subject (required for teachers)
        - region (string): Student region (required for students)
        - school (string): Student school (required for students)
        - class_id (string): Student class (required for students)
        - gender (string): Student gender (required for students)

        Returns:
        - 201: Success with JWT tokens and user details
        - 400: Validation errors
        """
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
    permission_classes = ()  # Autentifikatsiya talab qilinmaydi

    def post(self, request, *args, **kwargs):
        """
        Authenticate a user and return JWT tokens.

        POST request with the following parameters:
        - username (string): Phone number or email (required)
        - password (string): User password (required)

        Returns:
        - 200: Success with JWT tokens and user details
        - 401: Invalid credentials
        - 400: Validation errors
        """
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
        """
        Get all users (Teachers and Students).

        Returns:
        - 200: Success with user details
        """
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    