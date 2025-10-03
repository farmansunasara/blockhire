"""
URL configuration for verification app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.verify_document, name='verify_document'),
    path('status/<str:emp_id>/', views.verification_status, name='verification_status'),
    path('logs/<int:verification_id>/', views.verification_logs, name='verification_logs'),
    path('my-verifications/', views.my_verifications, name='my_verifications'),
]
