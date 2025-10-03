#!/usr/bin/env python
"""
Simple test script to verify backend API endpoints are working.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_backend():
    """Test backend API endpoints."""
    print("Testing BlockHire Backend API Integration...")
    print("=" * 50)
    
    # Test 1: Server availability
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
            "email": "flow_test_2025@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            print("   [OK] User registration successful")
            data = response.json()
            print(f"   Full response: {data}")
            if 'data' in data and 'user' in data['data']:
                user_data = data['data']['user']
                print(f"   User ID: {user_data.get('id')}")
                print(f"   Employee ID: {user_data.get('emp_id')}")
                print(f"   User Hash: {user_data.get('user_hash', '')[:16]}...")
                print(f"   Email: {user_data.get('email')}")
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
            print("   [OK] Login successful")
            data = response.json()
            print(f"   Full response: {data}")
            if 'data' in data and 'tokens' in data['data']:
                access_token = data['data']['tokens'].get('access', '')
                print(f"   Access Token: {access_token[:20]}...")
                return access_token
            return None
        else:
            print(f"   [ERROR] Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   [ERROR] Login error: {e}")
        return None

def main():
    """Run all tests."""
    print("BlockHire Backend Integration Test")
    print("=" * 50)
    
    # Test registration
    registration_result = test_backend()
    if not registration_result:
        print("\n[ERROR] Integration test failed at registration")
        return
    
    # Test login
    email = "flow_test_2025@example.com"
    password = "testpass123"
    token = test_login(email, password)
    if not token:
        print("\n[ERROR] Integration test failed at login")
        return
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Integration test completed!")
    print("\nBackend is ready for frontend integration!")
    print(f"Frontend should connect to: {BASE_URL}")
    print("\nNext steps:")
    print("1. Update frontend API calls to use real endpoints")
    print("2. Test user registration and login flow")
    print("3. Test profile management")
    print("4. Test document upload and verification")

if __name__ == "__main__":
    main()
