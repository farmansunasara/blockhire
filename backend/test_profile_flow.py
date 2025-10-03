#!/usr/bin/env python3
"""
Test Profile Flow - Frontend to Backend Integration
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_profile_flow():
    """Test complete profile flow."""
    print("BlockHire Profile Flow Test")
    print("=" * 50)
    
    # Test user login first
    email = "flow_test_2025@example.com"
    password = "testpass123"
    
    print(f"1. Logging in user: {email}")
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   [ERROR] Login failed: {response.text}")
        return
    
    data = response.json()
    access_token = data['data']['tokens']['access']
    print(f"   [OK] Login successful, token: {access_token[:20]}...")
    
    # Test profile loading
    print("\n2. Testing profile loading...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        profile_data = response.json()
        print(f"   [OK] Profile loaded successfully")
        print(f"   Full profile response: {json.dumps(profile_data, indent=2)}")
    else:
        print(f"   [ERROR] Profile loading failed: {response.text}")
        return
    
    # Test profile update
    print("\n3. Testing profile update...")
    update_data = {
        "first_name": "John",
        "last_name": "Doe",
        "mobile": "+1234567890",
        "address": "123 Test Street, Test City",
        "job_designation": "Software Developer",
        "department": "Engineering"
    }
    
    response = requests.put(f"{BASE_URL}/profile/update/", 
                          json=update_data, 
                          headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        updated_profile = response.json()
        print(f"   [OK] Profile updated successfully")
        print(f"   Updated profile: {json.dumps(updated_profile, indent=2)}")
    else:
        print(f"   [ERROR] Profile update failed: {response.text}")
        return
    
    # Test document upload
    print("\n4. Testing document upload...")
    
    # Create a simple test PDF content (this is just for testing)
    test_pdf_content = b"PDF test content for BlockHire integration test"
    
    files = {
        'file': ('test_document.pdf', test_pdf_content, 'application/pdf')
    }
    
    response = requests.post(f"{BASE_URL}/documents/upload/", 
                           files=files, 
                           headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        doc_data = response.json()
        print(f"   [OK] Document uploaded successfully")
        print(f"   Document response: {json.dumps(doc_data, indent=2)}")
    else:
        print(f"   [ERROR] Document upload failed: {response.text}")
        return
    
    print("\n" + "=" * 50)
    print("[SUCCESS] All profile flow tests completed!")
    print("Frontend-backend integration is working correctly!")

if __name__ == "__main__":
    test_profile_flow()
