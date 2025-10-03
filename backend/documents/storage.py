"""
Custom S3 storage configuration for document uploads.
"""
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import os


class DocumentStorage(S3Boto3Storage):
    """
    Custom S3 storage for documents with organized folder structure.
    """
    bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'blockhire-documents-prod')
    location = 'media/documents'
    file_overwrite = False
    default_acl = 'private'
    
    def get_valid_name(self, name):
        """
        Clean filename for S3 storage.
        """
        # Remove any path separators and clean the name
        name = os.path.basename(name)
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        return name
    
    def get_available_name(self, name, max_length=None):
        """
        Generate unique filename if file already exists.
        """
        if self.exists(name):
            # Add timestamp to make it unique
            import time
            name, ext = os.path.splitext(name)
            name = f"{name}_{int(time.time())}{ext}"
        return name


class PublicDocumentStorage(S3Boto3Storage):
    """
    Public S3 storage for documents that need public access.
    """
    bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'blockhire-documents-prod')
    location = 'media/documents'
    file_overwrite = False
    default_acl = 'public-read'
    
    def get_valid_name(self, name):
        """
        Clean filename for S3 storage.
        """
        name = os.path.basename(name)
        name = name.replace(' ', '_')
        return name
