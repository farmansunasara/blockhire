"""
Serializers for profile-related API endpoints.
"""
from rest_framework import serializers
from accounts.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    """
    email = serializers.CharField(source='user.email', read_only=True)
    user_hash = serializers.CharField(source='user.user_hash', read_only=True)
    emp_id = serializers.CharField(source='user.emp_id', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'user_hash', 'emp_id', 'first_name', 'last_name',
            'full_name', 'date_of_birth', 'mobile', 'address', 'job_designation',
            'department', 'doc_hash', 'doc_history', 'storage_path', 'is_profile_complete', 
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'email', 'user_hash', 'emp_id', 'doc_hash', 'doc_history',
            'created_at', 'updated_at'
        )
    
    def to_representation(self, instance):
        """
        Convert snake_case to camelCase for frontend compatibility.
        """
        data = super().to_representation(instance)
        return {
            'id': data['id'],
            'email': data['email'],
            'userHash': data['user_hash'],
            'empId': data['emp_id'],
            'firstName': data['first_name'],
            'lastName': data['last_name'],
            'fullName': data['full_name'],
            'dateOfBirth': data['date_of_birth'],
            'mobile': data['mobile'],
            'address': data['address'],
            'jobDesignation': data['job_designation'],
            'department': data['department'],
            'docHash': data['doc_hash'],
            'docHistory': data['doc_history'],
            'storagePath': data['storage_path'],
            'isProfileComplete': data['is_profile_complete'],
            'createdAt': data['created_at'],
            'updatedAt': data['updated_at']
        }
    
    def get_full_name(self, obj):
        return obj.full_name


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    dateOfBirth = serializers.DateField(source='date_of_birth', required=False)
    jobDesignation = serializers.CharField(source='job_designation', required=False)
    
    class Meta:
        model = UserProfile
        fields = (
            'firstName', 'lastName', 'dateOfBirth', 'mobile',
            'address', 'jobDesignation', 'department'
        )
    
    def update(self, instance, validated_data):
        """
        Update profile and mark as complete if all required fields are filled.
        """
        instance = super().update(instance, validated_data)
        
        # Check if profile is complete
        required_fields = [
            'first_name', 'last_name', 'date_of_birth',
            'mobile', 'address', 'job_designation', 'department'
        ]
        
        is_complete = all(
            getattr(instance, field) for field in required_fields
        )
        
        if is_complete and not instance.is_profile_complete:
            instance.is_profile_complete = True
            instance.save()
        
        return instance


class ProfileCompletionSerializer(serializers.Serializer):
    """
    Serializer for profile completion status.
    """
    is_complete = serializers.BooleanField()
    completion_percentage = serializers.IntegerField()
    missing_fields = serializers.ListField(child=serializers.CharField())
    completed_fields = serializers.ListField(child=serializers.CharField())
