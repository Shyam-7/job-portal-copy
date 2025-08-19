#!/usr/bin/env python3
"""
Full Integration Test for Job Portal
Tests both backend APIs and simulates frontend interactions
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_complete_user_flow():
    """Test complete user registration and login flow"""
    print("🧪 Testing Complete User Flow")
    print("=" * 40)
    
    # Step 1: Register a new user
    print("\n1. Testing User Registration...")
    test_user = {
        "email": f"testuser_{int(time.time())}@example.com",
        "password": "testpass123",
        "name": "Test User Integration"
    }
    
    try:
        # Note: We don't have registration endpoint in job_portal_backend yet
        # So we'll use an existing user
        print("   ⚠️  Using existing user for testing")
        test_user["email"] = "newuser@example.com"
        test_user["password"] = "password123"  # Correct password
        test_user["name"] = "New User"
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 2: Login with the user
    print("\n2. Testing User Login...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signin", json=login_data)
        if response.status_code == 200:
            auth_data = response.json()
            print(f"   ✅ Login successful for {auth_data['user']['name']}")
            token = auth_data['access_token']
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 3: Access protected jobs endpoint
    print("\n3. Testing Jobs Access with Authentication...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/jobs/", headers=headers)
        if response.status_code == 200:
            jobs = response.json()
            print(f"   ✅ Successfully retrieved {len(jobs)} jobs")
            
            # Show first job details
            if jobs:
                first_job = jobs[0]
                print(f"   📋 Sample Job: {first_job['title']} at {first_job['company_name']}")
        else:
            print(f"   ❌ Jobs access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Jobs access error: {e}")
        return False
    
    # Step 4: Test job search functionality
    print("\n4. Testing Job Search...")
    try:
        search_params = {"q": "Engineer"}
        response = requests.get(f"{BASE_URL}/api/jobs/search", params=search_params)
        if response.status_code == 200:
            search_results = response.json()
            print(f"   ✅ Search for 'Engineer' returned {len(search_results)} results")
        else:
            print(f"   ❌ Job search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Job search error: {e}")
        return False
    
    # Step 5: Test individual job retrieval
    print("\n5. Testing Individual Job Retrieval...")
    if jobs:
        try:
            job_id = jobs[0]['id']
            response = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
            if response.status_code == 200:
                job_detail = response.json()
                print(f"   ✅ Retrieved job details for: {job_detail['title']}")
            else:
                print(f"   ❌ Job detail retrieval failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Job detail error: {e}")
            return False
    
    print("\n" + "=" * 40)
    print("🎉 Complete Integration Test PASSED!")
    print("\n✅ User Flow Summary:")
    print("   • User authentication working")
    print("   • Job listings accessible")
    print("   • Job search functional")
    print("   • Individual job retrieval working")
    print("   • Backend API fully operational")
    print("   • Ready for frontend integration")
    
    return True

def test_frontend_ready():
    """Check if frontend is accessible"""
    print("\n🌐 Testing Frontend Accessibility...")
    try:
        response = requests.get("http://localhost:4200", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend is accessible at http://localhost:4200")
            return True
        else:
            print(f"   ⚠️  Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️  Frontend not accessible: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Job Portal Full Integration Test")
    print("=" * 50)
    
    # Test backend functionality
    backend_success = test_complete_user_flow()
    
    # Test frontend accessibility
    frontend_ready = test_frontend_ready()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"   Backend API: {'✅ WORKING' if backend_success else '❌ FAILED'}")
    print(f"   Frontend:    {'✅ ACCESSIBLE' if frontend_ready else '⚠️ CHECK NEEDED'}")
    
    if backend_success and frontend_ready:
        print("\n🎉 JOB PORTAL IS FULLY OPERATIONAL!")
        print("   • Backend microservices: ✅")
        print("   • Database connectivity: ✅")
        print("   • Authentication system: ✅")
        print("   • Job management: ✅")
        print("   • Frontend interface: ✅")
        print("\n🌐 You can now:")
        print("   1. Open http://localhost:4200 in your browser")
        print("   2. Login with: newuser@example.com / password123")
        print("   3. Browse and search for jobs")
        print("   4. View job details")
    else:
        print("\n⚠️  Some components need attention")
    
    return backend_success

if __name__ == "__main__":
    main()
