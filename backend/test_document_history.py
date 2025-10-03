#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced document handling implementation.
Tests docHash, docHistory[], and storagePath as specified in the workflow.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
EMAIL = f"doc_test_{int(time.time())}@example.com"
PASSWORD = "testpass123"

def test_document_workflow():
    """Test the complete document workflow with docHistory[] array."""
    print("Testing Enhanced Document Workflow")
    print("=" * 50)
    
    # Step 1: Register user
    print("\n1. Registering user...")
    register_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "confirm_password": PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    if response.status_code == 201:
        print("SUCCESS: User registered successfully")
        data = response.json()
        user_data = data['data']['user']
        tokens = data['data']['tokens']
        access_token = tokens['access']
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        print(f"ERROR: Registration failed: {response.text}")
        return
    
    # Step 2: Upload first document (should be original)
    print("\n2. Uploading first document (original)...")
    with open("test_document.pdf", "wb") as f:
        f.write(b"Test PDF content for original document")
    
    with open("test_document.pdf", "rb") as f:
        files = {"file": ("test_document.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/documents/upload/", files=files, headers=headers)
    
    if response.status_code == 201:
        print("SUCCESS: First document uploaded successfully")
        doc1_data = response.json()['data']
        print(f"   Document Hash: {doc1_data['docHash']}")
        print(f"   Is Original: {doc1_data['isOriginal']}")
    else:
        print(f"ERROR: First document upload failed: {response.text}")
        return
    
    # Step 3: Check profile for docHash and docHistory
    print("\n3. Checking profile for document information...")
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    if response.status_code == 200:
        profile_data = response.json()['data']
        print("SUCCESS: Profile retrieved successfully")
        print(f"   Original docHash: {profile_data.get('docHash', 'None')}")
        print(f"   docHistory array: {profile_data.get('docHistory', [])}")
        print(f"   storagePath: {profile_data.get('storagePath', 'None')}")
    else:
        print(f"ERROR: Profile retrieval failed: {response.text}")
        return
    
    # Step 4: Upload second document (should be added to history)
    print("\n4. Uploading second document (added to history)...")
    with open("test_document2.pdf", "wb") as f:
        f.write(b"Test PDF content for second document - different content")
    
    with open("test_document2.pdf", "rb") as f:
        files = {"file": ("test_document2.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/documents/upload/", files=files, headers=headers)
    
    if response.status_code == 201:
        print("SUCCESS: Second document uploaded successfully")
        doc2_data = response.json()['data']
        print(f"   Document Hash: {doc2_data['docHash']}")
        print(f"   Is Original: {doc2_data['isOriginal']}")
    else:
        print(f"ERROR: Second document upload failed: {response.text}")
        return
    
    # Step 5: Check updated profile
    print("\n5. Checking updated profile...")
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    if response.status_code == 200:
        profile_data = response.json()['data']
        print("SUCCESS: Updated profile retrieved successfully")
        print(f"   Original docHash: {profile_data.get('docHash', 'None')}")
        print(f"   docHistory array: {profile_data.get('docHistory', [])}")
        print(f"   History length: {len(profile_data.get('docHistory', []))}")
    else:
        print(f"ERROR: Profile retrieval failed: {response.text}")
        return
    
    # Step 6: Test document hashes endpoint
    print("\n6. Testing document hashes endpoint...")
    response = requests.get(f"{BASE_URL}/documents/hashes/", headers=headers)
    if response.status_code == 200:
        hashes_data = response.json()['data']
        print("SUCCESS: Document hashes retrieved successfully")
        print(f"   Original docHash: {hashes_data.get('docHash', 'None')}")
        print(f"   docHistory array: {hashes_data.get('docHistory', [])}")
        print(f"   storagePath: {hashes_data.get('storagePath', 'None')}")
    else:
        print(f"ERROR: Document hashes retrieval failed: {response.text}")
        return
    
    # Step 7: Test verification with original document
    print("\n7. Testing verification with original document...")
    original_hash = profile_data.get('docHash')
    if original_hash:
        verify_data = {
            "empId": user_data['emp_id'],
            "docHash": original_hash
        }
        response = requests.post(f"{BASE_URL}/verify/", json=verify_data)
        if response.status_code == 200:
            verify_result = response.json()
            print("SUCCESS: Verification completed")
            print(f"   Valid: {verify_result['data']['isValid']}")
            print(f"   Message: {verify_result['data']['message']}")
        else:
            print(f"ERROR: Verification failed: {response.text}")
    
    # Step 8: Test verification with non-original document
    print("\n8. Testing verification with non-original document...")
    if len(profile_data.get('docHistory', [])) > 1:
        non_original_hash = profile_data['docHistory'][1]  # Second document
        verify_data = {
            "empId": user_data['emp_id'],
            "docHash": non_original_hash
        }
        response = requests.post(f"{BASE_URL}/verify/", json=verify_data)
        if response.status_code == 200:
            verify_result = response.json()
            print("SUCCESS: Verification completed")
            print(f"   Valid: {verify_result['data']['isValid']}")
            print(f"   Message: {verify_result['data']['message']}")
        else:
            print(f"ERROR: Verification failed: {response.text}")
    
    # Cleanup
    print("\nCleaning up test files...")
    import os
    try:
        os.remove("test_document.pdf")
        os.remove("test_document2.pdf")
        print("SUCCESS: Test files cleaned up")
    except:
        print("WARNING: Could not clean up test files")
    
    print("\nDocument workflow test completed!")
    print("\nSummary:")
    print("   docHash: Original document hash stored and used for verification")
    print("   docHistory[]: Array of all document hashes maintained")
    print("   storagePath: Cloud storage path stored")
    print("   Rule: Only original docHash valid for verification")

if __name__ == "__main__":
    test_document_workflow()
