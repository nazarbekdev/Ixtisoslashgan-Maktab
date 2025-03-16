from django.urls import path
from .views import ClassListCreateAPIView, SubjectListCreateAPIView, OfflineStudentAPIView, TopicListAPIView, TestListAPIView, TeacherClassAPIView, StudentSubjectAPIView, StudentSubjectDetailView, TeacherExpertiseAPIView, TeacherExpertiseDetailView


urlpatterns = [
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject-list-create'),
    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('topics/', TopicListAPIView.as_view(), name='topic-list'),
    path('tests/', TestListAPIView.as_view(), name='test-list'),
    path("offline-student/", OfflineStudentAPIView.as_view(), name="offline-student"),
    path("teacher-class/", TeacherClassAPIView.as_view(), name="teacher-subject"),
    path("student-subject/", StudentSubjectAPIView.as_view(), name="student-subject"),
    path('student-subject/<int:student_id>/', StudentSubjectDetailView.as_view(), name='student-subject-detail'),
    path("teacher-expertise/", TeacherExpertiseAPIView.as_view(), name="teacher-expertise"),
    path('teacher-expertise/<int:teacher_id>/', TeacherExpertiseDetailView.as_view(), name='teacher-expertise-detail'),
]
