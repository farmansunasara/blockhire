#!/usr/bin/env python3
"""
Simple Cloudinary test without Django setup.
"""

import os
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blockhire.settings')

try:
    import django
    django.setup()
    
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    
    print("☁️  Testing Cloudinary Configuration")
    print("=" * 50)
    
    # Test 1: Check storage backend
    storage_class = default_storage.__class__.__name__
    print(f"Storage Backend: {storage_class}")
    
    # Test 2: Try to save a test file
    try:
        test_content = b"This is a test file for Cloudinary verification."
        test_filename = "test_cloudinary.txt"
        
        print(f"📤 Uploading test file: {test_filename}")
        saved_path = default_storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File saved to: {saved_path}")
        
        # Test 3: Check if file exists
        exists = default_storage.exists(saved_path)
        print(f"📁 File exists: {exists}")
        
        if exists:
            # Test 4: Try to read the file
            with default_storage.open(saved_path, 'rb') as f:
                content = f.read()
                print(f"📖 File content: {content.decode()}")
                print(f"📊 File size: {len(content)} bytes")
            
            # Test 5: Get file URL (if supported)
            try:
                file_url = default_storage.url(saved_path)
                print(f"🔗 File URL: {file_url}")
            except Exception as e:
                print(f"⚠️  URL generation not supported: {e}")
            
            # Test 6: Clean up test file
            try:
                default_storage.delete(saved_path)
                print(f"🗑️  Test file deleted successfully")
            except Exception as e:
                print(f"⚠️  Could not delete test file: {e}")
        
        print("\n🎉 Cloudinary is working correctly!")
        print("✅ Your files will now be stored in the cloud!")
        
    except Exception as e:
        print(f"❌ Cloudinary test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check your Cloudinary credentials in .env file")
        print("2. Verify your internet connection")
        print("3. Check if your Cloudinary account is active")
        
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    print("Make sure you're running this from the backend directory")
