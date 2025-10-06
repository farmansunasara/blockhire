"""
Account models for user authentication and management.
"""
import hashlib
import secrets
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model with additional fields for BlockHire system.
    """
    email = models.EmailField(unique=True)
    user_hash = models.CharField(max_length=64, unique=True, blank=True)
    emp_id = models.CharField(max_length=20, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'accounts_user'

    def save(self, *args, **kwargs):
        if not self.user_hash:
            self.user_hash = self.generate_user_hash()
        if not self.emp_id:
            self.emp_id = self.generate_emp_id()
        super().save(*args, **kwargs)

    def generate_user_hash(self):
        """Generate immutable user hash using SHA-256."""
        timestamp = str(int(timezone.now().timestamp()))
        random_salt = secrets.token_hex(16)
        hash_input = f"{self.email}{timestamp}{random_salt}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def generate_emp_id(self):
        """Generate unique employee ID."""
        timestamp = str(int(timezone.now().timestamp()))
        return f"EMP{timestamp[-6:]}"

    def __str__(self):
        return f"{self.email} ({self.emp_id})"


class UserProfile(models.Model):
    """
    Extended user profile with personal and employment information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Employment Information
    job_designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Document Information
    doc_hash = models.CharField(max_length=64, blank=True, null=True)  # Original valid hash
    doc_history = models.JSONField(default=list, blank=True)  # Array of all document hashes
    storage_path = models.CharField(max_length=500, blank=True, null=True)
    is_profile_complete = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.emp_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class JWTToken(models.Model):
    """
    JWT token storage for refresh tokens.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'jwt_tokens'

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at