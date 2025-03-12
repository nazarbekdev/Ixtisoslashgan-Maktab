from django.urls import path
from .views import StudentProfileAPIView, StudentProfileImageAPIView

urlpatterns = [
    path('student/profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('student/profile/image/', StudentProfileImageAPIView.as_view(), name='student-profile-image'),
]