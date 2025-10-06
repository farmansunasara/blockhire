#!/usr/bin/env python3
"""
Simple API test script for BlockHire backend
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api_connection():
    """Test basic API connectivity"""
    try:
        response = requests.get(f"{BASE_URL}/test/")
        print(f"✅ API Connection Test: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ API Connection Failed: {e}")
        return False

def test_registration():
    """Test user registration"""
    try:
        import time
        timestamp = int(time.time())
        data = {
            "email": f"test{timestamp}@example.com",
            "password": "testpassword123",
            "confirm_password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/register/", json=data)
        print(f"✅ Registration Test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Registration Failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        # Use the same email that was registered
        data = {
            "email": "test1759729808@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"✅ Login Test: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        
        if response.status_code == 200 and result.get('success'):
            # Store token for profile test
            token = result['data']['tokens']['access']
            return token
        return None
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return None

def test_profile(token):
    """Test profile endpoint with token"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        print(f"✅ Profile Test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Profile Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing BlockHire API...")
    print("=" * 50)
    
    # Test 1: Basic connectivity
    if not test_api_connection():
        print("❌ Cannot proceed - API not accessible")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test 2: Registration
    if not test_registration():
        print("❌ Registration failed")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test 3: Login
    token = test_login()
    if not token:
        print("❌ Login failed")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test 4: Profile with token
    if not test_profile(token):
        print("❌ Profile test failed")
        exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! API is working correctly.")
