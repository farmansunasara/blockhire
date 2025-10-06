"""
Cloud storage configuration for BlockHire.
Choose your preferred cloud storage provider.
"""

# =============================================================================
# CLOUDINARY CONFIGURATION (Recommended - 25GB Free)
# =============================================================================

# Step 1: Install dependencies
# pip install cloudinary django-cloudinary-storage

# Step 2: Add to settings.py
CLOUDINARY_CONFIG = {
    'cloud_name': 'your_cloud_name',  # Get from Cloudinary dashboard
    'api_key': 'your_api_key',        # Get from Cloudinary dashboard  
    'api_secret': 'your_api_secret',  # Get from Cloudinary dashboard
}

# Step 3: Update Django settings
DJANGO_SETTINGS_FOR_CLOUDINARY = """
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'cloudinary_storage',
    'cloudinary',
]

# Add cloudinary configuration
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage import CloudinaryStorage

cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key", 
    api_secret="your_api_secret"
)

# Use Cloudinary for file storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Remove local media settings (comment out)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
"""

# =============================================================================
# AWS S3 CONFIGURATION (5GB Free)
# =============================================================================

# Step 1: Install dependencies
# pip install boto3 django-storages

# Step 2: Update Django settings
DJANGO_SETTINGS_FOR_S3 = """
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'storages',
]

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Use S3 for file storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
"""

# =============================================================================
# BACKBLAZE B2 CONFIGURATION (10GB Free)
# =============================================================================

# Step 1: Install dependencies
# pip install boto3 django-storages

# Step 2: Update Django settings
DJANGO_SETTINGS_FOR_B2 = """
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'storages',
]

# Backblaze B2 Configuration
AWS_ACCESS_KEY_ID = 'your_b2_key_id'
AWS_SECRET_ACCESS_KEY = 'your_b2_application_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
AWS_S3_ENDPOINT_URL = 'https://s3.us-west-000.backblazeb2.com'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.us-west-000.backblazeb2.com'

# Use B2 for file storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
"""

# =============================================================================
# MIGRATION SCRIPT
# =============================================================================

def migrate_to_cloud_storage():
    """
    Script to help migrate existing files to cloud storage.
    """
    print("🔄 Migrating to Cloud Storage")
    print("=" * 50)
    
    print("1. Choose your cloud provider:")
    print("   - Cloudinary (25GB free) - Recommended")
    print("   - AWS S3 (5GB free)")
    print("   - Backblaze B2 (10GB free)")
    print()
    
    print("2. Follow the setup instructions above")
    print()
    
    print("3. Update your Django settings")
    print()
    
    print("4. Test the configuration:")
    print("   python manage.py shell")
    print("   >>> from django.core.files.storage import default_storage")
    print("   >>> default_storage.save('test.txt', ContentFile(b'test'))")
    print()
    
    print("5. Your files will now be stored in the cloud!")
    print("   - No more local media folder")
    print("   - Automatic CDN delivery")
    print("   - Scalable storage")

if __name__ == "__main__":
    migrate_to_cloud_storage()
