# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from store.views import RegistroView


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health, name='health'),
    path('api/auth/registro/', RegistroView.as_view(),        name='auth-registro'),
    path('api/auth/login/',    TokenObtainPairView.as_view(), name='auth-login'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(),    name='auth-refresh'),
    path('api/auth/logout/',   TokenBlacklistView.as_view(),  name='auth-logout'),
    path('api/', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)