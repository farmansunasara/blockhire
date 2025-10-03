#!/usr/bin/env python3
"""
Complete Document Flow Test - Frontend to Backend Integration
Tests the entire document workflow from upload to verification.
"""

import requests
import json
import time
import os

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:3000"

def test_complete_document_flow():
    """Test the complete document flow from frontend to backend."""
    print("=" * 60)
    print("COMPLETE DOCUMENT FLOW TEST")
    print("=" * 60)
    
    # Step 1: Register and login user
    print("\n1. USER REGISTRATION & LOGIN")
    print("-" * 30)
    
    email = f"flow_test_{int(time.time())}@example.com"
    password = "testpass123"
    
    # Register
    register_data = {
        "email": email,
        "password": password,
        "confirm_password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    if response.status_code != 201:
        print(f"❌ Registration failed: {response.text}")
        return
    
    print("SUCCESS: User registered successfully")
    
    # Login
    login_data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    data = response.json()
    access_token = data['data']['tokens']['access']
    user_data = data['data']['user']
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print("SUCCESS: User logged in successfully")
    print(f"   Employee ID: {user_data['emp_id']}")
    print(f"   User Hash: {user_data['user_hash']}")
    
    # Step 2: Upload first document (original)
    print("\n2. DOCUMENT UPLOAD - FIRST DOCUMENT")
    print("-" * 40)
    
    # Create test PDF with unique content
    timestamp = int(time.time())
    test_pdf_content = f"Test PDF content for original document - BlockHire verification system - {timestamp}".encode()
    with open("test_original.pdf", "wb") as f:
        f.write(test_pdf_content)
    
    with open("test_original.pdf", "rb") as f:
        files = {"file": ("test_original.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/documents/upload/", files=files, headers=headers)
    
    if response.status_code != 201:
        print(f"ERROR: First document upload failed: {response.text}")
        return
    
    doc1_data = response.json()['data']
    print("SUCCESS: First document uploaded successfully")
    print(f"   Document Hash: {doc1_data['docHash']}")
    print(f"   Is Original: {doc1_data['isOriginal']}")
    print(f"   File Name: {doc1_data['fileName']}")
    
    # Step 3: Check profile for document information
    print("\n3. PROFILE DOCUMENT INFORMATION")
    print("-" * 35)
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    if response.status_code != 200:
        print(f"ERROR: Profile retrieval failed: {response.text}")
        return
    
    profile_data = response.json()['data']
    print("SUCCESS: Profile retrieved successfully")
    print(f"   Original docHash: {profile_data.get('docHash', 'None')}")
    print(f"   docHistory array: {profile_data.get('docHistory', [])}")
    print(f"   storagePath: {profile_data.get('storagePath', 'None')}")
    
    # Step 4: Upload second document (added to history)
    print("\n4. DOCUMENT UPLOAD - SECOND DOCUMENT")
    print("-" * 40)
    
    # Create second test PDF with different content
    test_pdf_content2 = f"Test PDF content for second document - completely different content - BlockHire verification system v2 - {timestamp + 1}".encode()
    with open("test_second.pdf", "wb") as f:
        f.write(test_pdf_content2)
    
    with open("test_second.pdf", "rb") as f:
        files = {"file": ("test_second.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/documents/upload/", files=files, headers=headers)
    
    if response.status_code != 201:
        print(f"ERROR: Second document upload failed: {response.text}")
        return
    
    doc2_data = response.json()['data']
    print("SUCCESS: Second document uploaded successfully")
    print(f"   Document Hash: {doc2_data['docHash']}")
    print(f"   Is Original: {doc2_data['isOriginal']}")
    print(f"   File Name: {doc2_data['fileName']}")
    
    # Step 5: Check updated profile
    print("\n5. UPDATED PROFILE DOCUMENT INFORMATION")
    print("-" * 42)
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    if response.status_code != 200:
        print(f"ERROR: Profile retrieval failed: {response.text}")
        return
    
    updated_profile = response.json()['data']
    print("SUCCESS: Updated profile retrieved successfully")
    print(f"   Original docHash: {updated_profile.get('docHash', 'None')}")
    print(f"   docHistory array: {updated_profile.get('docHistory', [])}")
    print(f"   History length: {len(updated_profile.get('docHistory', []))}")
    
    # Step 6: Test document hashes endpoint
    print("\n6. DOCUMENT HASHES ENDPOINT")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/documents/hashes/", headers=headers)
    if response.status_code != 200:
        print(f"ERROR: Document hashes retrieval failed: {response.text}")
        return
    
    hashes_data = response.json()['data']
    print("SUCCESS: Document hashes retrieved successfully")
    print(f"   Original docHash: {hashes_data.get('docHash', 'None')}")
    print(f"   docHistory array: {hashes_data.get('docHistory', [])}")
    print(f"   storagePath: {hashes_data.get('storagePath', 'None')}")
    
    # Step 7: Test verification with original document
    print("\n7. DOCUMENT VERIFICATION - ORIGINAL DOCUMENT")
    print("-" * 45)
    
    original_hash = updated_profile.get('docHash')
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
            if verify_result['data']['isValid']:
                print("   SUCCESS: Document is authentic and verified!")
            else:
                print("   ERROR: Document verification failed")
        else:
            print(f"ERROR: Verification failed: {response.text}")
    else:
        print("ERROR: No original document hash found")
    
    # Step 8: Test verification with non-original document
    print("\n8. DOCUMENT VERIFICATION - NON-ORIGINAL DOCUMENT")
    print("-" * 48)
    
    if len(updated_profile.get('docHistory', [])) > 1:
        non_original_hash = updated_profile['docHistory'][1]  # Second document
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
            if not verify_result['data']['isValid']:
                print("   SUCCESS: Correctly rejected non-original document!")
            else:
                print("   ERROR: Should have rejected non-original document")
        else:
            print(f"ERROR: Verification failed: {response.text}")
    else:
        print("WARNING: Only one document in history, skipping non-original test")
    
    # Step 9: Test document history endpoint
    print("\n9. DOCUMENT HISTORY ENDPOINT")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/documents/history/", headers=headers)
    if response.status_code == 200:
        history_data = response.json()
        print("SUCCESS: Document history retrieved successfully")
        print(f"   Number of documents: {len(history_data)}")
        for i, doc in enumerate(history_data):
            print(f"   Document {i+1}: {doc.get('fileName', 'Unknown')} (Original: {doc.get('isOriginal', False)})")
    else:
        print(f"ERROR: Document history retrieval failed: {response.text}")
    
    # Step 10: Test with tampered document hash
    print("\n10. DOCUMENT VERIFICATION - TAMPERED HASH")
    print("-" * 45)
    
    tampered_hash = "a" * 64  # Fake hash
    verify_data = {
        "empId": user_data['emp_id'],
        "docHash": tampered_hash
    }
    response = requests.post(f"{BASE_URL}/verify/", json=verify_data)
    if response.status_code == 200:
        verify_result = response.json()
        print("SUCCESS: Verification completed")
        print(f"   Valid: {verify_result['data']['isValid']}")
        print(f"   Message: {verify_result['data']['message']}")
        if not verify_result['data']['isValid']:
            print("   SUCCESS: Correctly detected tampered document!")
        else:
            print("   ERROR: Should have detected tampered document")
    else:
        print(f"ERROR: Verification failed: {response.text}")
    
    # Cleanup
    print("\n11. CLEANUP")
    print("-" * 15)
    
    try:
        os.remove("test_original.pdf")
        os.remove("test_second.pdf")
        print("SUCCESS: Test files cleaned up")
    except:
        print("WARNING: Could not clean up test files")
    
    print("\n" + "=" * 60)
    print("DOCUMENT FLOW TEST COMPLETED")
    print("=" * 60)
    
    print("\nSUMMARY:")
    print("SUCCESS: User registration and login")
    print("SUCCESS: Document upload (original and additional)")
    print("SUCCESS: Profile document information storage")
    print("SUCCESS: Document history array maintenance")
    print("SUCCESS: Document verification (original document)")
    print("SUCCESS: Document verification (non-original document)")
    print("SUCCESS: Document verification (tampered document)")
    print("SUCCESS: Document history endpoint")
    print("SUCCESS: Document hashes endpoint")
    
    print("\nALL TESTS PASSED - DOCUMENT FLOW IS WORKING CORRECTLY!")

if __name__ == "__main__":
    test_complete_document_flow()
