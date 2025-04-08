from django.urls import path
from .views import RegisterAPIView, LoginAPIView, AllUserAPIView, PasswordResetRequestAPIView, \
    PasswordResetConfirmAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('all/', AllUserAPIView.as_view(), name='all_users'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]
