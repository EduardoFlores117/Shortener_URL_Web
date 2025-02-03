from django.contrib import admin
from django.urls import path, include
from shortener.views import home_redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),  # ✅ Incluye todas las rutas de la app `shortener`
]

# Sirve archivos en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

