"""
URL configuration for profiles app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_profile, name='get_profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('complete/', views.complete_profile, name='complete_profile'),
    path('completion-status/', views.profile_completion_status, name='profile_completion_status'),
]
