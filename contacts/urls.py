from django.urls import path
from .views import ContactRequestListAPIView

urlpatterns = [
    path('contact-request/', ContactRequestListAPIView.as_view(), name='contact-request'),
]