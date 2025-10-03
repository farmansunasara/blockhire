"""
Admin configuration for documents app.
"""
from django.contrib import admin
from .models import DocumentRecord, DocumentVersion, DocumentAccessLog


@admin.register(DocumentRecord)
class DocumentRecordAdmin(admin.ModelAdmin):
    """
    Admin configuration for DocumentRecord model.
    """
    list_display = ('file_name', 'user', 'doc_hash_short', 'file_size_mb', 'is_original', 'upload_date')
    list_filter = ('is_original', 'file_type', 'upload_date')
    search_fields = ('file_name', 'user__email', 'user__emp_id', 'doc_hash')
    ordering = ('-upload_date',)
    
    fieldsets = (
        ('Document Information', {'fields': ('user', 'file_name', 'doc_hash', 'file_size', 'file_type')}),
        ('Storage', {'fields': ('storage_path', 'is_original')}),
        ('Metadata', {'fields': ('upload_ip', 'user_agent', 'upload_date')}),
    )
    
    readonly_fields = ('doc_hash', 'upload_date', 'upload_ip', 'user_agent')
    
    def doc_hash_short(self, obj):
        return f"{obj.doc_hash[:16]}..." if obj.doc_hash else "N/A"
    doc_hash_short.short_description = "Document Hash"


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    """
    Admin configuration for DocumentVersion model.
    """
    list_display = ('document', 'version_number', 'file_name', 'file_size', 'upload_date')
    list_filter = ('version_number', 'upload_date')
    search_fields = ('document__file_name', 'document__user__email')
    ordering = ('-upload_date',)
    
    readonly_fields = ('upload_date',)


@admin.register(DocumentAccessLog)
class DocumentAccessLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for DocumentAccessLog model.
    """
    list_display = ('document', 'accessed_by', 'access_type', 'access_date', 'ip_address')
    list_filter = ('access_type', 'access_date')
    search_fields = ('document__file_name', 'accessed_by__email', 'ip_address')
    ordering = ('-access_date',)
    
    readonly_fields = ('access_date',)