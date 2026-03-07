"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from gallery.views import home, about, upload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('upload/', upload, name='upload'),
]

# Добавляем маршруты для медиа-файлов (работает при любом DEBUG)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)