"""
Verification models for document authenticity checking.
"""
from django.db import models
from django.utils import timezone


class VerificationRequest(models.Model):
    """
    Track document verification requests.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    emp_id = models.CharField(max_length=20)
    doc_hash = models.CharField(max_length=64)
    requested_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='verification_requests', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verification_date = models.DateTimeField(blank=True, null=True)
    result_message = models.TextField(blank=True, null=True)
    is_valid = models.BooleanField(default=False)
    
    # Additional metadata
    request_ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'verification_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f"Verification {self.emp_id} - {self.status}"

    def mark_verified(self, message="Document verified successfully"):
        """Mark verification as successful."""
        self.status = 'verified'
        self.is_valid = True
        self.verification_date = timezone.now()
        self.result_message = message
        self.save()

    def mark_failed(self, message="Document verification failed"):
        """Mark verification as failed."""
        self.status = 'failed'
        self.is_valid = False
        self.verification_date = timezone.now()
        self.result_message = message
        self.save()


class VerificationResult(models.Model):
    """
    Store detailed verification results.
    """
    verification_request = models.OneToOneField(VerificationRequest, on_delete=models.CASCADE, related_name='result')
    employee_details = models.JSONField(blank=True, null=True)
    document_preview_url = models.URLField(blank=True, null=True)
    download_url = models.URLField(blank=True, null=True)
    verification_metadata = models.JSONField(blank=True, null=True)
    
    class Meta:
        db_table = 'verification_results'

    def __str__(self):
        return f"Result for {self.verification_request.emp_id}"


class VerificationLog(models.Model):
    """
    Log all verification activities for auditing.
    """
    verification_request = models.ForeignKey(VerificationRequest, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50)
    details = models.TextField(blank=True, null=True)
    performed_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        db_table = 'verification_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} - {self.verification_request.emp_id}"