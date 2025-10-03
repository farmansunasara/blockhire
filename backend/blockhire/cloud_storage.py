"""
Cloud storage configuration for BlockHire.
Supports AWS S3, Google Cloud Storage, and local storage.
"""
import os
from django.conf import settings

# Cloud storage settings
CLOUD_STORAGE_PROVIDER = os.getenv('CLOUD_STORAGE_PROVIDER', 'local')  # 's3', 'gcs', 'local'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'blockhire-documents')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_DEFAULT_ACL = 'private'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True

# Google Cloud Storage Configuration
GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME', 'blockhire-documents')
GS_PROJECT_ID = os.getenv('GS_PROJECT_ID')

# File upload settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
ALLOWED_MIME_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png'
]

def get_storage_config():
    """Get storage configuration based on provider."""
    if CLOUD_STORAGE_PROVIDER == 's3':
        return {
            'DEFAULT_FILE_STORAGE': 'storages.backends.s3boto3.S3Boto3Storage',
            'STATICFILES_STORAGE': 'storages.backends.s3boto3.S3StaticStorage',
            'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
            'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
            'AWS_STORAGE_BUCKET_NAME': AWS_STORAGE_BUCKET_NAME,
            'AWS_S3_REGION_NAME': AWS_S3_REGION_NAME,
            'AWS_S3_CUSTOM_DOMAIN': AWS_S3_CUSTOM_DOMAIN,
            'AWS_DEFAULT_ACL': AWS_DEFAULT_ACL,
            'AWS_S3_FILE_OVERWRITE': AWS_S3_FILE_OVERWRITE,
            'AWS_S3_VERIFY': AWS_S3_VERIFY,
        }
    elif CLOUD_STORAGE_PROVIDER == 'gcs':
        return {
            'DEFAULT_FILE_STORAGE': 'storages.backends.gcloud.GoogleCloudStorage',
            'STATICFILES_STORAGE': 'storages.backends.gcloud.GoogleCloudStaticStorage',
            'GS_BUCKET_NAME': GS_BUCKET_NAME,
            'GS_PROJECT_ID': GS_PROJECT_ID,
        }
    else:  # local
        return {
            'DEFAULT_FILE_STORAGE': 'django.core.files.storage.FileSystemStorage',
        }
