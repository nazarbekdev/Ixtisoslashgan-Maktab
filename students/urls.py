from django.urls import path
from .views import StudentProfileAPIView, StudentProfileImageAPIView, SubmitAssignmentAPIView, TestTypeListCreateAPIView, TestResultListCreateAPIView, TestResultDetailView

urlpatterns = [
    path('profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('profile/image/', StudentProfileImageAPIView.as_view(), name='student-profile-image'),
    path('submit-assignment/', SubmitAssignmentAPIView.as_view(), name='submit-assignment'),
    path('test-types/', TestTypeListCreateAPIView.as_view(), name='test-types'),
    path('test-results/', TestResultListCreateAPIView.as_view(), name='test-results'),
    path('test-results/<int:student_id>/', TestResultDetailView.as_view(), name='test-result-detail'),
]