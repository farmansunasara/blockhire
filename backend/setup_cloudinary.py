#!/usr/bin/env python3
"""
Cloudinary Setup Script for BlockHire
"""

import os

def create_env_file():
    """Create .env file with Cloudinary configuration."""
    
    env_content = """# Django Settings
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,blockhire-backend.onrender.com

# Database
DATABASE_URL=sqlite:///db.sqlite3

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# Cloudinary Settings (Get these from your Cloudinary dashboard)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://blockhire-frontend.onrender.com

# File Upload Settings
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=pdf

# Rate Limiting
RATE_LIMIT_ENABLE=True
RATE_LIMIT_PER_MINUTE=60
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with Cloudinary configuration")
    print("📝 Please update the Cloudinary credentials in .env file")

def setup_instructions():
    """Print setup instructions."""
    
    print("🚀 Cloudinary Setup Instructions")
    print("=" * 50)
    print()
    print("1. 📝 Get your Cloudinary credentials:")
    print("   - Go to: https://cloudinary.com/console")
    print("   - Copy your Cloud Name, API Key, and API Secret")
    print()
    print("2. 🔧 Update your .env file:")
    print("   - Open backend/.env")
    print("   - Replace the placeholder values:")
    print("     CLOUDINARY_CLOUD_NAME=your_actual_cloud_name")
    print("     CLOUDINARY_API_KEY=your_actual_api_key")
    print("     CLOUDINARY_API_SECRET=your_actual_api_secret")
    print()
    print("3. 🧪 Test the configuration:")
    print("   python test_cloud_storage.py")
    print()
    print("4. 🚀 Start your server:")
    print("   python manage.py runserver")
    print()
    print("5. 📤 Upload a document to test cloud storage!")
    print()
    print("🎉 Your files will now be stored in Cloudinary!")

if __name__ == "__main__":
    create_env_file()
    setup_instructions()
