"""
Serializers for document-related API endpoints.
"""
from rest_framework import serializers
from .models import DocumentRecord, DocumentVersion, DocumentAccessLog


class DocumentUploadSerializer(serializers.Serializer):
    """
    Serializer for document upload.
    """
    file = serializers.FileField()
    
    def validate_file(self, value):
        """
        Validate uploaded file.
        """
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("File size cannot exceed 10MB")
        
        # Check file type
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF, JPEG, and PNG files are allowed")
        
        return value


class DocumentRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for document records.
    """
    file_size_mb = serializers.ReadOnlyField()
    download_url = serializers.ReadOnlyField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentRecord
        fields = [
            'id', 'doc_hash', 'upload_date', 'file_name', 'file_size',
            'file_size_mb', 'is_original', 'storage_path', 'file_type',
            'download_url', 'user_name'
        ]
        read_only_fields = ['id', 'doc_hash', 'upload_date', 'user']
    
    def get_user_name(self, obj):
        """Get user's full name."""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email


class DocumentHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for document history.
    """
    file_size_mb = serializers.ReadOnlyField()
    download_url = serializers.ReadOnlyField()
    
    class Meta:
        model = DocumentRecord
        fields = [
            'id', 'doc_hash', 'upload_date', 'file_name', 'file_size',
            'file_size_mb', 'is_original', 'storage_path', 'file_type',
            'download_url'
        ]


class DocumentAccessLogSerializer(serializers.ModelSerializer):
    """
    Serializer for document access logs.
    """
    class Meta:
        model = DocumentAccessLog
        fields = [
            'id', 'access_type', 'access_date', 'ip_address', 'user_agent'
        ]


class DocumentVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for document versions.
    """
    class Meta:
        model = DocumentVersion
        fields = [
            'id', 'version_number', 'doc_hash', 'file_name', 'file_size',
            'storage_path', 'upload_date', 'change_reason'
        ]