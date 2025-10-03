"""
URL configuration for documents app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.DocumentUploadView.as_view(), name='document_upload'),
    path('history/', views.document_history, name='document_history'),
    path('hashes/', views.document_hashes, name='document_hashes'),
    path('download/<str:doc_hash>/', views.download_document, name='download_document'),
    path('details/<str:doc_hash>/', views.document_details, name='document_details'),
    path('delete/<str:doc_hash>/', views.delete_document, name='delete_document'),
    path('access-logs/<str:doc_hash>/', views.access_logs, name='access_logs'),
]
