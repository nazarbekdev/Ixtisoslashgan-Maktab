from django.urls import path
from .views import MaterialListCreateView, MaterialDetailView, TeacherProfileAPIView, MaterialNameDetailView, \
    MaterialByClassSubjectView, MaterialTeacherDetailView, TestUploadView, TestListView

urlpatterns = [
    path('profile/', TeacherProfileAPIView.as_view(), name='teacher-profile'),
    path('materials/', MaterialListCreateView.as_view(), name='material-list-create'),
    path('materials/<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
    path('materials/name/<int:material_id>/', MaterialNameDetailView.as_view(), name='material-name-detail'),
    path('materials/<int:class_id>/<int:subject_id>/', MaterialByClassSubjectView.as_view(),
         name='material-by-subject-class'),
    path('materials/details/<int:teacher_id>/', MaterialTeacherDetailView.as_view(), name='material-detail'),
    path('tests/', TestUploadView.as_view(), name='test-upload'),
    path('tests/details/<int:teacher_id>/', TestListView.as_view(), name='test-list'),
]
