#!/usr/bin/env python
"""
Test script to verify backend API endpoints are working.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test all API endpoints."""
    print("Testing BlockHire Backend API Integration...")
    print("=" * 50)
    
    # Test 1: Health check (if we had one)
    print("1. Testing server availability...")
    try:
        response = requests.get(f"{BASE_URL}/auth/")
        print(f"   [OK] Server is running (Status: {response.status_code})")
    except Exception as e:
        print(f"   [ERROR] Server not accessible: {e}")
        return False
    
    # Test 2: User Registration
    print("\n2. Testing user registration...")
    try:
        registration_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "confirmPassword": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print("   [OK] User registration successful")
            data = response.json()
            print(f"   User ID: {data.get('user', {}).get('id')}")
            print(f"   Employee ID: {data.get('user', {}).get('emp_id')}")
            print(f"   User Hash: {data.get('user', {}).get('user_hash')[:16]}...")
            return data
        else:
            print(f"   [ERROR] Registration failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   [ERROR] Registration error: {e}")
        return None

def test_login(email, password):
    """Test user login."""
    print("\n3. Testing user login...")
    try:
        login_data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Login successful")
            data = response.json()
            print(f"   Access Token: {data.get('tokens', {}).get('access', '')[:20]}...")
            return data.get('tokens', {}).get('access')
        else:
            print(f"   ❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return None

def test_profile_endpoints(token):
    """Test profile-related endpoints."""
    print("\n4. Testing profile endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test get profile
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        print(f"   Get Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Profile retrieval successful")
            profile_data = response.json()
            print(f"   Profile ID: {profile_data.get('id')}")
            print(f"   Name: {profile_data.get('first_name')} {profile_data.get('last_name')}")
        else:
            print(f"   ❌ Profile retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Profile test error: {e}")

def test_verification_endpoints():
    """Test verification endpoints."""
    print("\n5. Testing verification endpoints...")
    
    try:
        # Test document verification
        verification_data = {
            "emp_id": "EMP123456",
            "doc_hash": "test_hash_1234567890abcdef"
        }
        
        response = requests.post(f"{BASE_URL}/verify/", json=verification_data)
        print(f"   Verification Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Verification endpoint accessible")
            data = response.json()
            print(f"   Result: {data.get('is_valid', False)}")
            print(f"   Message: {data.get('message', 'No message')}")
        else:
            print(f"   ❌ Verification failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Verification test error: {e}")

def main():
    """Run all tests."""
    print("🚀 BlockHire Backend Integration Test")
    print("=" * 50)
    
    # Test registration
    registration_result = test_api_endpoints()
    if not registration_result:
        print("\n❌ Integration test failed at registration")
        return
    
    # Test login
    email = "test@example.com"
    password = "testpass123"
    token = test_login(email, password)
    if not token:
        print("\n❌ Integration test failed at login")
        return
    
    # Test profile endpoints
    test_profile_endpoints(token)
    
    # Test verification endpoints
    test_verification_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Integration test completed!")
    print("\nBackend is ready for frontend integration!")
    print(f"Frontend should connect to: {BASE_URL}")
    print("\nNext steps:")
    print("1. Update frontend API calls to use real endpoints")
    print("2. Test user registration and login flow")
    print("3. Test profile management")
    print("4. Test document upload and verification")

if __name__ == "__main__":
    main()
