"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, JWTToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for User model.
    """
    list_display = ('email', 'emp_id', 'user_hash', 'first_name', 'last_name', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'emp_id', 'user_hash', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_hash', 'emp_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('user_hash', 'emp_id', 'created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = ('user', 'full_name', 'job_designation', 'department', 'is_profile_complete', 'created_at')
    list_filter = ('is_profile_complete', 'department', 'created_at')
    search_fields = ('user__email', 'user__emp_id', 'first_name', 'last_name', 'job_designation')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'date_of_birth', 'mobile', 'address')}),
        ('Employment Information', {'fields': ('job_designation', 'department')}),
        ('Document Information', {'fields': ('doc_hash', 'storage_path', 'is_profile_complete')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JWTToken)
class JWTTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for JWTToken model.
    """
    list_display = ('user', 'created_at', 'expires_at', 'is_revoked', 'is_expired')
    list_filter = ('is_revoked', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__emp_id')
    ordering = ('-created_at',)
    
    readonly_fields = ('user', 'token', 'created_at', 'expires_at')