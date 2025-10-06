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
        fields = [
            'id', 'issuer_id', 'name', 'email', 'company',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IssuerAuthorizationSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer authorizations.
    """
    issuer_name = serializers.CharField(source='issuer.name', read_only=True)
    employee_name = serializers.SerializerMethodField()
    
    class Meta:
        model = IssuerAuthorization
        fields = [
            'id', 'issuer', 'issuer_name', 'emp_id', 'user_hash',
            'employee', 'employee_name', 'status', 'permission_granted',
            'granted_at', 'revoked_at', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_employee_name(self, obj):
        """Get employee's full name."""
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}".strip() or obj.employee.email
        return None


class IssuerAuthorizationRequestSerializer(serializers.Serializer):
    """
    Serializer for authorization requests.
    """
    emp_id = serializers.CharField(max_length=20)
    user_hash = serializers.CharField(max_length=64)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_emp_id(self, value):
        """Validate employee ID format."""
        if not value.startswith('EMP'):
            raise serializers.ValidationError("Employee ID must start with 'EMP'")
        return value


class IssuerAccessLogSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer access logs.
    """
    class Meta:
        model = IssuerAccessLog
        fields = [
            'id', 'action', 'emp_id', 'user_hash', 'doc_hash',
            'details', 'ip_address', 'user_agent', 'timestamp'
        ]


class IssuerSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for issuer settings.
    """
    class Meta:
        model = IssuerSettings
        fields = [
            'id', 'max_authorizations', 'auto_approve', 'require_verification',
            'notification_email', 'settings_json'
        ]


class EmployeeDetailsSerializer(serializers.Serializer):
    """
    Serializer for employee details response.
    """
    empId = serializers.CharField()
    userHash = serializers.CharField()
    email = serializers.EmailField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    jobDesignation = serializers.CharField()
    department = serializers.CharField()
    isProfileComplete = serializers.BooleanField()
    hasOriginalDocument = serializers.BooleanField()
    createdAt = serializers.DateTimeField()
    updatedAt = serializers.DateTimeField()