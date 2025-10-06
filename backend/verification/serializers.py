"""
Serializers for verification-related API endpoints.
"""
from rest_framework import serializers
from .models import VerificationRequest, VerificationResult, VerificationLog


class DocumentVerificationSerializer(serializers.Serializer):
    """
    Serializer for document verification requests.
    """
    emp_id = serializers.CharField(max_length=20)
    doc_hash = serializers.CharField(max_length=64)
    
    def validate_emp_id(self, value):
        """Validate employee ID format."""
        if not value.startswith('EMP'):
            raise serializers.ValidationError("Employee ID must start with 'EMP'")
        return value
    
    def validate_doc_hash(self, value):
        """Validate document hash format."""
        if len(value) != 64:
            raise serializers.ValidationError("Document hash must be 64 characters long")
        return value


class VerificationResponseSerializer(serializers.Serializer):
    """
    Serializer for verification responses.
    """
    is_valid = serializers.BooleanField()
    message = serializers.CharField()
    verification_date = serializers.DateTimeField()


class VerificationRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for verification requests.
    """
    class Meta:
        model = VerificationRequest
        fields = [
            'id', 'emp_id', 'doc_hash', 'status', 'verification_date',
            'result_message', 'is_valid', 'request_ip', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class VerificationResultSerializer(serializers.ModelSerializer):
    """
    Serializer for verification results.
    """
    class Meta:
        model = VerificationResult
        fields = [
            'id', 'employee_details', 'document_preview_url',
            'download_url', 'verification_metadata'
        ]


class VerificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for verification logs.
    """
    class Meta:
        model = VerificationLog
        fields = [
            'id', 'action', 'details', 'performed_by', 'timestamp',
            'ip_address'
        ]