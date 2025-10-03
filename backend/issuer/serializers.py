"""
Serializers for issuer-related API endpoints.
"""
from rest_framework import serializers
from .models import Issuer, IssuerAuthorization, IssuerAccessLog, IssuerSettings


class IssuerSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer data.
    """
    class Meta:
        model = Issuer
        fields = (
            'id', 'issuer_id', 'name', 'email', 'company',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'issuer_id', 'created_at', 'updated_at')


class IssuerAuthorizationSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer authorizations.
    """
    issuer_name = serializers.CharField(source='issuer.name', read_only=True)
    employee_name = serializers.SerializerMethodField()
    
    class Meta:
        model = IssuerAuthorization
        fields = (
            'id', 'issuer', 'issuer_name', 'emp_id', 'user_hash',
            'employee', 'employee_name', 'status', 'permission_granted',
            'granted_at', 'revoked_at', 'reason', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'issuer_name', 'employee_name', 'granted_at',
            'revoked_at', 'created_at', 'updated_at'
        )
    
    def get_employee_name(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return "Unknown"


class IssuerAuthorizationRequestSerializer(serializers.Serializer):
    """
    Serializer for authorization requests.
    """
    # Accept both camelCase and snake_case for frontend compatibility
    empId = serializers.CharField(max_length=20, source='emp_id')
    userHash = serializers.CharField(max_length=64, source='user_hash')
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate_empId(self, value):
        """
        Validate employee ID format.
        """
        if not value.startswith('EMP'):
            raise serializers.ValidationError("Invalid employee ID format")
        return value
    
    def validate_userHash(self, value):
        """
        Validate user hash format.
        """
        if len(value) != 64:
            raise serializers.ValidationError("Invalid user hash format")
        return value


class IssuerAccessLogSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer access logs.
    """
    class Meta:
        model = IssuerAccessLog
        fields = (
            'id', 'action', 'emp_id', 'user_hash', 'doc_hash',
            'details', 'ip_address', 'timestamp'
        )
        read_only_fields = ('id', 'timestamp')


class IssuerSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer settings.
    """
    class Meta:
        model = IssuerSettings
        fields = (
            'id', 'max_authorizations', 'auto_approve',
            'require_verification', 'notification_email', 'settings_json'
        )


class EmployeeDetailsSerializer(serializers.Serializer):
    """
    Serializer for employee details response.
    """
    emp_id = serializers.CharField()
    user_hash = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    job_designation = serializers.CharField()
    department = serializers.CharField()
    is_profile_complete = serializers.BooleanField()
    has_original_document = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
