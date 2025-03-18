from django.urls import path
from .views import MaterialListCreateView, MaterialDetailView, TeacherProfileAPIView

urlpatterns = [
    path('profile/', TeacherProfileAPIView.as_view(), name='teacher-profile'),
    path('materials/', MaterialListCreateView.as_view(), name='material-list-create'),
    path('materials/<int:pk>/', MaterialDetailView.as_view(), name='material-detail'),
]