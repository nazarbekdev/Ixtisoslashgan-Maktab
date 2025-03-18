from django.urls import path
from .views import StudentProfileAPIView, StudentProfileImageAPIView, SubmitAssignmentAPIView, TestTypeListCreateAPIView, TestResultListCreateAPIView, TestResultDetailView, StudentProfileByIdAPIView, StudentSubmitAssignmentAPIView, StudentRatingAPIView

urlpatterns = [
    path('profile/', StudentProfileAPIView.as_view(), name='student-profile'),
    path('profile/<int:student_id>/', StudentProfileByIdAPIView.as_view(), name='student-profile-by-id'),
    path('profile/image/', StudentProfileImageAPIView.as_view(), name='student-profile-image'),
    path('rating/<int:student_id>/', StudentRatingAPIView.as_view(), name='student-rating'),
    path('submit-assignment/', SubmitAssignmentAPIView.as_view(), name='submit-assignment'),
    path('submit-assignment/<int:student_id>/', StudentSubmitAssignmentAPIView.as_view(), name='submit-assignment-by-student'),
    path('test-types/', TestTypeListCreateAPIView.as_view(), name='test-types'),
    path('test-results/', TestResultListCreateAPIView.as_view(), name='test-results'),
    path('test-results/<int:student_id>/', TestResultDetailView.as_view(), name='test-result-detail'),
]