"""
Serializers for verification-related API endpoints.
"""
from rest_framework import serializers
from .models import VerificationRequest, VerificationResult, VerificationLog


class VerificationRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for verification requests.
    """
    class Meta:
        model = VerificationRequest
        fields = (
            'id', 'emp_id', 'doc_hash', 'status', 'verification_date',
            'result_message', 'is_valid', 'created_at'
        )
        read_only_fields = (
            'id', 'status', 'verification_date', 'result_message',
            'is_valid', 'created_at'
        )


class VerificationResultSerializer(serializers.ModelSerializer):
    """
    Serializer for verification results.
    """
    verification_request = VerificationRequestSerializer(read_only=True)
    
    class Meta:
        model = VerificationResult
        fields = (
            'id', 'verification_request', 'employee_details',
            'document_preview_url', 'download_url', 'verification_metadata'
        )


class VerificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for verification logs.
    """
    performed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VerificationLog
        fields = (
            'id', 'action', 'details', 'performed_by_name',
            'timestamp', 'ip_address'
        )
        read_only_fields = ('id', 'timestamp', 'performed_by_name')
    
    def get_performed_by_name(self, obj):
        if obj.performed_by:
            return f"{obj.performed_by.first_name} {obj.performed_by.last_name}"
        return "System"


class DocumentVerificationSerializer(serializers.Serializer):
    """
    Serializer for document verification input.
    """
    # Accept camelCase for frontend compatibility
    empId = serializers.CharField(max_length=20, source='emp_id')
    docHash = serializers.CharField(max_length=64, source='doc_hash')
    
    def validate_empId(self, value):
        """
        Validate employee ID format.
        """
        if not value.startswith('EMP'):
            raise serializers.ValidationError("Invalid employee ID format")
        return value
    
    def validate_docHash(self, value):
        """
        Validate document hash format.
        """
        if len(value) != 64:
            raise serializers.ValidationError("Invalid document hash format")
        return value


class VerificationResponseSerializer(serializers.Serializer):
    """
    Serializer for verification response.
    """
    is_valid = serializers.BooleanField()
    message = serializers.CharField()
    employee_details = serializers.DictField(required=False)
    document_preview = serializers.URLField(required=False)
    download_link = serializers.URLField(required=False)
    verification_date = serializers.DateTimeField()
