from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Ixtisoslashgan Maktab API",
        default_version='v1',
        description="API for managing teachers, students, and classes",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Hamma uchun ochiq
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # /api/token/
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # /api/token/refresh/
    path('auth/', include('accounts.urls')), # accounts uchun URL’lar
    path('courses/', include('courses.urls')), # courses uchun URL’lar
    path('news/', include('news.urls')), # news uchun URL’lar
    path('contacts/', include('contacts.urls')), # contacts uchun URL’lar
    path('students/', include('students.urls')), # students uchun URL’lar
    path('teachers/', include('teachers.urls')), # teachers uchun URL’lar 
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
