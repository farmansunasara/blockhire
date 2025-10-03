"""
Document models for file upload and management.
"""
import hashlib
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.conf import settings
from .storage import DocumentStorage


class DocumentRecord(models.Model):
    """
    Model to store document information and metadata.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='documents')
    doc_hash = models.CharField(max_length=64, unique=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    is_original = models.BooleanField(default=False)
    storage_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=10, default='pdf')
    
    # S3 File field for cloud storage
    file = models.FileField(
        upload_to='documents/',
        storage=DocumentStorage(),
        blank=True,
        null=True,
        help_text="Uploaded document file"
    )
    
    # Additional metadata
    upload_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'document_records'
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.file_name} ({self.doc_hash[:16]}...)"

    def save(self, *args, **kwargs):
        if not self.doc_hash:
            self.doc_hash = self.generate_doc_hash()
        super().save(*args, **kwargs)

    def generate_doc_hash(self):
        """Generate SHA-256 hash for the document."""
        # This should be called after file is uploaded
        # For now, generate a placeholder hash
        content = f"{self.user.user_hash}{self.file_name}{self.upload_date}"
        return hashlib.sha256(content.encode()).hexdigest()

    @property
    def file_size_mb(self):
        """Return file size in MB."""
        return round(self.file_size / (1024 * 1024), 2)

    @property
    def download_url(self):
        """Generate download URL for the document."""
        return f"/api/documents/download/{self.doc_hash}/"


class DocumentVersion(models.Model):
    """
    Track document versions and changes.
    """
    document = models.ForeignKey(DocumentRecord, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    doc_hash = models.CharField(max_length=64)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    storage_path = models.CharField(max_length=500)
    upload_date = models.DateTimeField(auto_now_add=True)
    change_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'document_versions'
        unique_together = ['document', 'version_number']
        ordering = ['-version_number']

    def __str__(self):
        return f"{self.document.file_name} v{self.version_number}"


class DocumentAccessLog(models.Model):
    """
    Log document access for security and auditing.
    """
    document = models.ForeignKey(DocumentRecord, on_delete=models.CASCADE, related_name='access_logs')
    accessed_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    access_type = models.CharField(max_length=20, choices=[
        ('view', 'View'),
        ('download', 'Download'),
        ('verify', 'Verify'),
    ])
    access_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'document_access_logs'
        ordering = ['-access_date']

    def __str__(self):
        return f"{self.document.file_name} - {self.access_type} by {self.accessed_by.email}"