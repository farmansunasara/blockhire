"""
Admin configuration for verification app.
"""
from django.contrib import admin
from .models import VerificationRequest, VerificationResult, VerificationLog


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for VerificationRequest model.
    """
    list_display = ('emp_id', 'doc_hash_short', 'status', 'is_valid', 'verification_date', 'created_at')
    list_filter = ('status', 'is_valid', 'created_at', 'verification_date')
    search_fields = ('emp_id', 'doc_hash', 'result_message')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Verification Details', {'fields': ('emp_id', 'doc_hash', 'requested_by')}),
        ('Result', {'fields': ('status', 'is_valid', 'verification_date', 'result_message')}),
        ('Metadata', {'fields': ('request_ip', 'user_agent', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'verification_date')
    
    def doc_hash_short(self, obj):
        return f"{obj.doc_hash[:16]}..." if obj.doc_hash else "N/A"
    doc_hash_short.short_description = "Document Hash"


@admin.register(VerificationResult)
class VerificationResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for VerificationResult model.
    """
    list_display = ('verification_request', 'has_employee_details', 'has_preview_url', 'has_download_url')
    search_fields = ('verification_request__emp_id', 'verification_request__doc_hash')
    
    fieldsets = (
        ('Verification Request', {'fields': ('verification_request',)}),
        ('Result Data', {'fields': ('employee_details', 'document_preview_url', 'download_url')}),
        ('Metadata', {'fields': ('verification_metadata',)}),
    )
    
    def has_employee_details(self, obj):
        return bool(obj.employee_details)
    has_employee_details.boolean = True
    has_employee_details.short_description = "Has Employee Details"
    
    def has_preview_url(self, obj):
        return bool(obj.document_preview_url)
    has_preview_url.boolean = True
    has_preview_url.short_description = "Has Preview URL"
    
    def has_download_url(self, obj):
        return bool(obj.download_url)
    has_download_url.boolean = True
    has_download_url.short_description = "Has Download URL"


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for VerificationLog model.
    """
    list_display = ('verification_request', 'action', 'performed_by', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('verification_request__emp_id', 'performed_by__email', 'ip_address')
    ordering = ('-timestamp',)
    
    readonly_fields = ('timestamp',)