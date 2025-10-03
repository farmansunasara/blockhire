"""
Admin configuration for issuer app.
"""
from django.contrib import admin
from .models import Issuer, IssuerAuthorization, IssuerAccessLog, IssuerSettings


@admin.register(Issuer)
class IssuerAdmin(admin.ModelAdmin):
    """
    Admin configuration for Issuer model.
    """
    list_display = ('name', 'company', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'company', 'issuer_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {'fields': ('issuer_id', 'name', 'email', 'company')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('issuer_id', 'created_at', 'updated_at')


@admin.register(IssuerAuthorization)
class IssuerAuthorizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for IssuerAuthorization model.
    """
    list_display = ('issuer', 'emp_id', 'employee_name', 'status', 'permission_granted', 'created_at')
    list_filter = ('status', 'permission_granted', 'created_at')
    search_fields = ('issuer__name', 'emp_id', 'user_hash', 'employee__email')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Authorization Details', {'fields': ('issuer', 'emp_id', 'user_hash', 'employee')}),
        ('Status', {'fields': ('status', 'permission_granted', 'reason')}),
        ('Timestamps', {'fields': ('granted_at', 'revoked_at', 'created_at', 'updated_at')}),
        ('Created By', {'fields': ('created_by',)}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'granted_at', 'revoked_at')
    
    def employee_name(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return "N/A"
    employee_name.short_description = "Employee Name"


@admin.register(IssuerAccessLog)
class IssuerAccessLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for IssuerAccessLog model.
    """
    list_display = ('issuer', 'action', 'emp_id', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('issuer__name', 'emp_id', 'user_hash', 'ip_address')
    ordering = ('-timestamp',)
    
    readonly_fields = ('timestamp',)


@admin.register(IssuerSettings)
class IssuerSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for IssuerSettings model.
    """
    list_display = ('issuer', 'max_authorizations', 'auto_approve', 'require_verification')
    search_fields = ('issuer__name', 'issuer__email')
    
    fieldsets = (
        ('Issuer', {'fields': ('issuer',)}),
        ('Settings', {'fields': ('max_authorizations', 'auto_approve', 'require_verification')}),
        ('Notifications', {'fields': ('notification_email',)}),
        ('Custom Settings', {'fields': ('settings_json',)}),
    )