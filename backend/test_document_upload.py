#!/usr/bin/env python3
"""
Test Document Upload - Debug Original Document Setting
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_document_upload():
    """Test document upload and original document setting."""
    print("Document Upload Test")
    print("=" * 30)
    
    # Step 1: Register and login as user
    print("1. Registering user...")
    timestamp = int(time.time())
    registration_data = {
        "email": f"doc_test_{timestamp}@example.com",
        "password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 201:
        print(f"   [ERROR] Registration failed: {response.text}")
        return
    
    data = response.json()
    access_token = data['data']['tokens']['access']
    user_data = data['data']['user']
    print(f"   [OK] User registered: {user_data.get('emp_id')}")
    
    # Step 2: Complete profile
    print("\n2. Completing profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_data = {
        "firstName": "Test",
        "lastName": "User",
        "mobile": "+1234567890",
        "address": "123 Test Street",
        "jobDesignation": "Test Engineer",
        "department": "Testing"
    }
    
    response = requests.put(f"{BASE_URL}/profile/update/", 
                          json=profile_data, 
                          headers=headers)
    print(f"   Profile update status: {response.status_code}")
    
    # Step 3: Upload document
    print("\n3. Uploading document...")
    test_doc_content = f"Test document content - {timestamp}".encode()
    files = {
        'file': ('test_document.pdf', test_doc_content, 'application/pdf')
    }
    
    response = requests.post(f"{BASE_URL}/documents/upload/", 
                           files=files, 
                           headers=headers)
    print(f"   Document upload status: {response.status_code}")
    
    if response.status_code == 201:
        doc_response = response.json()
        print(f"   [OK] Document uploaded")
        print(f"   Response: {json.dumps(doc_response, indent=2)}")
        
        # Step 4: Check profile for doc_hash
        print("\n4. Checking profile for doc_hash...")
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        print(f"   Profile status: {response.status_code}")
        
        if response.status_code == 200:
            profile_response = response.json()
            profile_data = profile_response.get('data', {})
            doc_hash = profile_data.get('docHash')
            print(f"   Profile doc_hash: {doc_hash}")
            
            if doc_hash:
                print(f"   [SUCCESS] Document hash saved to profile!")
            else:
                print(f"   [ERROR] Document hash not saved to profile")
        else:
            print(f"   [ERROR] Failed to get profile: {response.text}")
    else:
        print(f"   [ERROR] Document upload failed: {response.text}")

if __name__ == "__main__":
    test_document_upload()
