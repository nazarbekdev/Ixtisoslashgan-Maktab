from django.urls import path
from .views import ClassListCreateAPIView, SubjectListCreateAPIView, OfflineStudentAPIView, TopicListAPIView, TestListAPIView

urlpatterns = [
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject-list-create'),
    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('topics/', TopicListAPIView.as_view(), name='topic-list'),
    path('tests/', TestListAPIView.as_view(), name='test-list'),
    path("offline-student/", OfflineStudentAPIView.as_view(), name="offline-student"),
]
