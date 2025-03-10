from django.urls import path
from .views import ClassListCreateAPIView, SubjectListCreateAPIView, OfflineStudentAPIView

urlpatterns = [
    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject-list-create'),
    path("offline-student/", OfflineStudentAPIView.as_view(), name="offline-student"),
]
