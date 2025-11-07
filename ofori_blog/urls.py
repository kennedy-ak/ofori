"""
URL configuration for ofori_blog project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    # Home
    path('', home_view, name='home'),

    # Users app
    path('', include('users.urls')),

    # Blog app
    path('', include('blog.urls')),

    # Newsletter app
    path('newsletter/', include('newsletter.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
