"""
URL configuration for issuer app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.authorize_employee, name='authorize_employee'),
    path('employee-details/', views.get_employee_details, name='get_employee_details'),
    path('authorized/', views.authorized_employees, name='authorized_employees'),
    path('revoke/<str:emp_id>/', views.revoke_authorization, name='revoke_authorization'),
    path('access-logs/', views.access_logs, name='access_logs'),
    path('settings/', views.issuer_settings, name='issuer_settings'),
]
