#!/usr/bin/env python3
"""
Test script to verify job application functionality
"""
import requests
import json
import sys

def test_job_application_functionality():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Testing Job Application Functionality")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False
    
    # Test 2: Get available jobs
    try:
        response = requests.get(f"{base_url}/api/jobs/", timeout=5)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Jobs API working - Found {len(jobs)} jobs")
            if len(jobs) > 0:
                job_id = jobs[0]['id']
                print(f"   Sample job: {jobs[0]['title']} at {jobs[0]['company_name']}")
            else:
                print("❌ No jobs available")
                return False
        else:
            print(f"❌ Jobs API failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Jobs API error: {e}")
        return False
    
    # Test 3: Get current user applications
    try:
        response = requests.get(f"{base_url}/api/applications/user", timeout=5)
        if response.status_code == 200:
            applications = response.json()
            print(f"✅ Applications API working - Found {len(applications)} applications")
            for app in applications:
                print(f"   Applied to: {app.get('job_title', 'Unknown')} - Status: {app.get('status', 'Unknown')}")
        else:
            print(f"❌ Applications API failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Applications API error: {e}")
        return False
    
    # Test 4: Try to create a new application
    try:
        # Create application payload
        application_data = {
            "job_id": job_id,
            "cover_letter": "I am very interested in this position and believe my skills would be a great fit.",
            "resume_url": "https://example.com/resume.pdf"
        }
        
        response = requests.post(
            f"{base_url}/api/applications/", 
            json=application_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            new_app = response.json()
            print("✅ Application creation working")
            print(f"   Created application ID: {new_app['id']}")
            print(f"   Status: {new_app['status']}")
        elif response.status_code == 400:
            error_detail = response.json().get('detail', 'Unknown error')
            if "already applied" in error_detail:
                print("✅ Application creation working (already applied - expected)")
            else:
                print(f"❌ Application creation failed: {error_detail}")
                return False
        else:
            print(f"❌ Application creation failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Application creation error: {e}")
        return False
    
    print("=" * 50)
    print("🎉 All job application functionality tests passed!")
    return True

if __name__ == "__main__":
    success = test_job_application_functionality()
    sys.exit(0 if success else 1)
