# Cloud Storage Setup Guide

## 🎯 Recommended: Cloudinary (25GB Free)

### Step 1: Create Cloudinary Account
1. Go to [cloudinary.com](https://cloudinary.com)
2. Click "Sign Up for Free"
3. **No credit card required**
4. Get your credentials from dashboard

### Step 2: Install Dependencies
```bash
pip install cloudinary django-cloudinary-storage
```

### Step 3: Update Django Settings
```python
# backend/blockhire/settings.py

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage import CloudinaryStorage

# Cloudinary configuration
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key", 
    api_secret="your_api_secret"
)

# Update storage settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Remove local media settings
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Step 4: Update Requirements
```bash
# Add to requirements.txt
cloudinary==1.36.0
django-cloudinary-storage==0.3.0
```

## 🔄 Alternative: AWS S3 (5GB Free)

### Step 1: Create AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Create free account (no credit card for free tier)
3. Create S3 bucket

### Step 2: Install Dependencies
```bash
pip install boto3 django-storages
```

### Step 3: Update Django Settings
```python
# backend/blockhire/settings.py

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
```

## 🔄 Alternative: Backblaze B2 (10GB Free)

### Step 1: Create Backblaze Account
1. Go to [backblaze.com](https://backblaze.com)
2. Create free account
3. Create B2 bucket

### Step 2: Install Dependencies
```bash
pip install boto3 django-storages
```

### Step 3: Update Django Settings
```python
# backend/blockhire/settings.py

# Backblaze B2 Configuration
AWS_ACCESS_KEY_ID = 'your_b2_key_id'
AWS_SECRET_ACCESS_KEY = 'your_b2_application_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
AWS_S3_ENDPOINT_URL = 'https://s3.us-west-000.backblazeb2.com'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.us-west-000.backblazeb2.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

## 📊 Comparison Table

| Service | Free Storage | Free Bandwidth | Credit Card | Ease of Use |
|---------|-------------|----------------|-------------|-------------|
| **Cloudinary** | 25GB | 25GB/month | ❌ No | ⭐⭐⭐⭐⭐ |
| **AWS S3** | 5GB | 20K requests | ❌ No | ⭐⭐⭐⭐ |
| **Backblaze B2** | 10GB | 1GB/day | ❌ No | ⭐⭐⭐⭐ |
| **Google Cloud** | 5GB | 1GB/month | ❌ No | ⭐⭐⭐ |

## 🚀 Quick Start (Cloudinary)

1. **Sign up**: [cloudinary.com](https://cloudinary.com)
2. **Get credentials**: Dashboard → Settings → API Keys
3. **Install**: `pip install cloudinary django-cloudinary-storage`
4. **Configure**: Update settings.py
5. **Deploy**: Your files will be stored in the cloud!

## 💡 Benefits of Cloud Storage

- ✅ **Scalability**: No storage limits
- ✅ **Reliability**: 99.9% uptime
- ✅ **CDN**: Fast global delivery
- ✅ **Backup**: Automatic redundancy
- ✅ **Security**: Enterprise-grade
- ✅ **Cost**: Free tier covers most needs
