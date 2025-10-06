"""
URL configuration for accounts app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_endpoint, name='test_endpoint'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/refresh/', views.refresh_token, name='refresh_token'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/complete/', views.complete_profile, name='complete_profile'),
    path('user/', views.user_info, name='user_info'),
]
