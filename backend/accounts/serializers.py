"""
Serializers for account-related API endpoints.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile
from .authentication import generate_tokens


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        """
        Validate password confirmation.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        """
        Create new user with hashed password.
        """
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        # Set default values for first_name and last_name
        validated_data['first_name'] = validated_data.get('first_name', '')
        validated_data['last_name'] = validated_data.get('last_name', '')
        
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            **validated_data
        )
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """
        Validate user credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'user_hash', 'emp_id', 'first_name', 'last_name',
            'full_name', 'is_verified', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user_hash', 'emp_id', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    """
    full_name = serializers.SerializerMethodField()
    # Include user fields directly for flat structure
    email = serializers.CharField(source='user.email', read_only=True)
    user_hash = serializers.CharField(source='user.user_hash', read_only=True)
    emp_id = serializers.CharField(source='user.emp_id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'user_hash', 'emp_id', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'mobile', 'address', 'job_designation',
            'department', 'doc_hash', 'doc_history', 'storage_path', 'is_profile_complete',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'email', 'user_hash', 'emp_id', 'doc_hash', 'doc_history', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return obj.full_name


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = UserProfile
        fields = (
            'first_name', 'last_name', 'date_of_birth', 'mobile',
            'address', 'job_designation', 'department'
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


class TokenSerializer(serializers.Serializer):
    """
    Serializer for JWT tokens.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    access_expires_in = serializers.IntegerField()
    refresh_expires_in = serializers.IntegerField()


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer for login response.
    """
    user = UserSerializer()
    tokens = TokenSerializer()
    message = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for token refresh.
    """
    refresh = serializers.CharField()
    
    def validate_refresh(self, value):
        """
        Validate refresh token.
        """
        from .authentication import refresh_access_token
        try:
            return refresh_access_token(value)
        except Exception as e:
            raise serializers.ValidationError(str(e))
