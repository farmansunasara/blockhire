"""
Issuer models for employee authorization and management.
"""
from django.db import models
from django.utils import timezone


class Issuer(models.Model):
    """
    Model for issuers (HR departments, companies).
    """
    issuer_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'issuers'

    def __str__(self):
        return f"{self.name} ({self.company})"


class IssuerAuthorization(models.Model):
    """
    Track employee authorizations by issuers.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revoked', 'Revoked'),
    ]
    
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, related_name='authorizations')
    emp_id = models.CharField(max_length=20)
    user_hash = models.CharField(max_length=64)
    employee = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='authorizations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    permission_granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_authorizations')
    
    class Meta:
        db_table = 'issuer_authorizations'
        unique_together = ['issuer', 'emp_id', 'user_hash']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.issuer.name} - {self.emp_id} ({self.status})"

    def approve(self, reason="Approved by issuer"):
        """Approve the authorization."""
        self.status = 'approved'
        self.permission_granted = True
        self.granted_at = timezone.now()
        self.reason = reason
        self.save()

    def reject(self, reason="Rejected by issuer"):
        """Reject the authorization."""
        self.status = 'rejected'
        self.permission_granted = False
        self.reason = reason
        self.save()

    def revoke(self, reason="Revoked by issuer"):
        """Revoke the authorization."""
        self.status = 'revoked'
        self.permission_granted = False
        self.revoked_at = timezone.now()
        self.reason = reason
        self.save()


class IssuerAccessLog(models.Model):
    """
    Log issuer access activities for auditing.
    """
    ACTION_CHOICES = [
        ('authorize', 'Authorize Employee'),
        ('verify', 'Verify Document'),
        ('view_profile', 'View Employee Profile'),
        ('download_document', 'Download Document'),
        ('revoke_access', 'Revoke Access'),
    ]
    
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, related_name='access_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    emp_id = models.CharField(max_length=20, blank=True, null=True)
    user_hash = models.CharField(max_length=64, blank=True, null=True)
    doc_hash = models.CharField(max_length=64, blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'issuer_access_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.issuer.name} - {self.action} - {self.timestamp}"


class IssuerSettings(models.Model):
    """
    Store issuer-specific settings and preferences.
    """
    issuer = models.OneToOneField(Issuer, on_delete=models.CASCADE, related_name='settings')
    max_authorizations = models.PositiveIntegerField(default=1000)
    auto_approve = models.BooleanField(default=False)
    require_verification = models.BooleanField(default=True)
    notification_email = models.EmailField(blank=True, null=True)
    settings_json = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'issuer_settings'

    def __str__(self):
        return f"Settings for {self.issuer.name}"