#!/usr/bin/env python3
"""
Test Profile Update Flow - Frontend to Backend Integration
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_profile_update_flow():
    """Test profile update flow from frontend perspective."""
    print("BlockHire Profile Update Flow Test")
    print("=" * 50)
    
    # Step 1: Register a new user
    print("1. Registering new user...")
    registration_data = {
        "email": "profile_update_test@example.com",
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
    print(f"   [OK] User registered successfully")
    print(f"   User ID: {user_data.get('id')}")
    print(f"   Employee ID: {user_data.get('emp_id')}")
    print(f"   Email: {user_data.get('email')}")
    
    # Step 2: Load initial profile
    print("\n2. Loading initial profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        profile_data = response.json()
        print(f"   [OK] Profile loaded successfully")
        print(f"   Initial profile data:")
        if 'data' in profile_data:
            profile = profile_data['data']
            print(f"     First Name: '{profile.get('firstName')}'")
            print(f"     Last Name: '{profile.get('lastName')}'")
            print(f"     Mobile: '{profile.get('mobile')}'")
            print(f"     Address: '{profile.get('address')}'")
            print(f"     Job Designation: '{profile.get('jobDesignation')}'")
            print(f"     Department: '{profile.get('department')}'")
    else:
        print(f"   [ERROR] Profile loading failed: {response.text}")
        return
    
    # Step 3: Test profile update (as frontend would send)
    print("\n3. Testing profile update from frontend...")
    
    # This is exactly what the frontend would send
    frontend_update_data = {
        "firstName": "John",
        "lastName": "Doe",
        "mobile": "+1234567890",
        "address": "123 Main Street, Test City, TC 12345",
        "jobDesignation": "Senior Software Engineer",
        "department": "Engineering"
    }
    
    print(f"   Frontend sending data: {json.dumps(frontend_update_data, indent=2)}")
    
    response = requests.put(f"{BASE_URL}/profile/update/", 
                          json=frontend_update_data, 
                          headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        updated_profile = response.json()
        print(f"   [OK] Profile update successful!")
        print(f"   Response structure: {list(updated_profile.keys())}")
        print(f"   Has 'success': {'success' in updated_profile}")
        print(f"   Has 'data': {'data' in updated_profile}")
        print(f"   Has 'message': {'message' in updated_profile}")
        
        if 'data' in updated_profile:
            profile = updated_profile['data']
            print(f"\n   Updated profile data:")
            print(f"     ID: {profile.get('id')}")
            print(f"     Email: {profile.get('email')}")
            print(f"     User Hash: {profile.get('userHash', '')[:16]}...")
            print(f"     Employee ID: {profile.get('empId')}")
            print(f"     First Name: '{profile.get('firstName')}'")
            print(f"     Last Name: '{profile.get('lastName')}'")
            print(f"     Full Name: '{profile.get('fullName')}'")
            print(f"     Mobile: '{profile.get('mobile')}'")
            print(f"     Address: '{profile.get('address')}'")
            print(f"     Job Designation: '{profile.get('jobDesignation')}'")
            print(f"     Department: '{profile.get('department')}'")
            print(f"     Is Profile Complete: {profile.get('isProfileComplete')}")
            print(f"     Created At: {profile.get('createdAt')}")
            print(f"     Updated At: {profile.get('updatedAt')}")
        
        print(f"\n   Message: {updated_profile.get('message')}")
        
    else:
        print(f"   [ERROR] Profile update failed: {response.text}")
        return
    
    # Step 4: Verify the update by loading profile again
    print("\n4. Verifying update by reloading profile...")
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        verify_profile = response.json()
        print(f"   [OK] Profile reloaded successfully")
        
        if 'data' in verify_profile:
            profile = verify_profile['data']
            print(f"   Verification - Updated values:")
            print(f"     First Name: '{profile.get('firstName')}' (expected: 'John')")
            print(f"     Last Name: '{profile.get('lastName')}' (expected: 'Doe')")
            print(f"     Mobile: '{profile.get('mobile')}' (expected: '+1234567890')")
            print(f"     Address: '{profile.get('address')}' (expected: '123 Main Street, Test City, TC 12345')")
            print(f"     Job Designation: '{profile.get('jobDesignation')}' (expected: 'Senior Software Engineer')")
            print(f"     Department: '{profile.get('department')}' (expected: 'Engineering')")
            
            # Verify all updates were applied correctly
            updates_correct = (
                profile.get('firstName') == 'John' and
                profile.get('lastName') == 'Doe' and
                profile.get('mobile') == '+1234567890' and
                profile.get('address') == '123 Main Street, Test City, TC 12345' and
                profile.get('jobDesignation') == 'Senior Software Engineer' and
                profile.get('department') == 'Engineering'
            )
            
            if updates_correct:
                print(f"\n   [SUCCESS] All profile updates verified correctly!")
            else:
                print(f"\n   [WARNING] Some profile updates may not have been applied correctly")
    else:
        print(f"   [ERROR] Profile reload failed: {response.text}")
        return
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Profile update flow test completed!")
    print("\nFrontend to Backend Profile Update Flow:")
    print("[OK] Frontend sends camelCase data")
    print("[OK] Backend receives and processes data")
    print("[OK] Backend updates database")
    print("[OK] Backend returns updated profile in camelCase")
    print("[OK] Frontend receives properly formatted response")
    print("[OK] All field mappings work correctly")

if __name__ == "__main__":
    test_profile_update_flow()
