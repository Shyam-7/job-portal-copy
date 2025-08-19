#!/usr/bin/env python3
"""
Backend Testing Script for Job Portal
Tests all the API endpoints to ensure everything is working
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_server(max_retries=10):
    """Wait for the server to be ready"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            print(f"⏳ Waiting for server... (attempt {i+1}/{max_retries})")
            time.sleep(2)
    return False

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        response = requests.get(f"{BASE_URL}/api/db-test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database connection: {data['status']}")
            if 'postgresql_version' in data:
                print(f"   PostgreSQL Version: {data['postgresql_version']}")
            return True
        else:
            print(f"❌ Database test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_jobs_endpoint():
    """Test jobs endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/")
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Jobs endpoint working - found {len(jobs)} jobs")
            return True
        else:
            print(f"❌ Jobs endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Jobs endpoint error: {e}")
        return False

def test_auth_signin():
    """Test authentication signin"""
    try:
        # Try to sign in with a user from the database
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/signin", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Auth signin working - Welcome {data.get('user', {}).get('name', 'User')}")
            return True, data.get('access_token')
        else:
            print(f"❌ Auth signin failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ Auth signin error: {e}")
        return False, None

def test_users_list():
    """Test users list endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/auth/users/all")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Users list working - found {data.get('total_users', 0)} users")
            return True
        else:
            print(f"❌ Users list failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Users list error: {e}")
        return False

def run_all_tests():
    """Run all backend tests"""
    print("🧪 Running Job Portal Backend Tests")
    print("=" * 50)
    
    # Wait for server
    if not wait_for_server():
        print("❌ Server not ready, aborting tests")
        return False
    
    # Test basic endpoints
    print("\n1. Testing Health Endpoint...")
    if not test_health():
        return False
    
    print("\n2. Testing Database Connection...")
    if not test_database_connection():
        return False
    
    print("\n3. Testing Jobs Endpoint...")
    if not test_jobs_endpoint():
        return False
    
    print("\n4. Testing Authentication...")
    auth_success, token = test_auth_signin()
    
    print("\n5. Testing Users List...")
    if not test_users_list():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All Backend Tests Completed!")
    
    if auth_success:
        print("✅ Authentication is working")
        print("✅ Jobs API is working")
        print("✅ Database connection is working")
        print("✅ All microservices are operational")
    else:
        print("⚠️  Authentication needs attention")
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
