from django.urls import path
from .views import StudentProfileAPIView, StudentProfileImageAPIView, SubmitAssignmentAPIView

urlpatterns = [
    path('profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('profile/image/', StudentProfileImageAPIView.as_view(), name='student-profile-image'),
    path('submit-assignment/', SubmitAssignmentAPIView.as_view(), name='submit-assignment'),
]