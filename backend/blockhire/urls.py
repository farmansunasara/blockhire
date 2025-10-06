"""
URL configuration for blockhire project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # This includes the test endpoint
    path('api/auth/', include('accounts.urls')),
    path('api/profile/', include('profiles.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/verify/', include('verification.urls')),
    path('api/issuer/', include('issuer.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)