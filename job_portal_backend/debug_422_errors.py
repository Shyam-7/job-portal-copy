#!/usr/bin/env python3
"""
Debug script to identify 422 errors in job application functionality
"""
import requests
import json

def test_endpoints():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Testing Job Application Endpoints for 422 Errors")
    print("=" * 60)
    
    # Test 1: Applied jobs endpoint
    print("\n1. Testing Applied Jobs Endpoint")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/applications/user", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            applications = response.json()
            print(f"✅ SUCCESS: Found {len(applications)} applications")
            for app in applications:
                print(f"   - {app.get('job_title', 'Unknown')} ({app.get('status', 'Unknown')})")
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {e}")
    
    # Test 2: Get available jobs for application
    print("\n2. Testing Jobs Endpoint")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/api/jobs/", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ SUCCESS: Found {len(jobs)} jobs")
            test_job_id = jobs[0]['id'] if jobs else None
            print(f"Test Job ID: {test_job_id}")
            return test_job_id
        else:
            print(f"❌ ERROR {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ REQUEST ERROR: {e}")
        return None

def test_job_application(job_id):
    base_url = "http://127.0.0.1:8000"
    
    print("\n3. Testing Job Application (Quick Apply)")
    print("-" * 40)
    
    # Test quick apply
    quick_apply_data = {
        "job_id": job_id
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/applications/",
            json=quick_apply_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Quick Apply Status: {response.status_code}")
        print(f"Quick Apply Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ 422 UNPROCESSABLE CONTENT ERROR - Invalid request format")
            
    except Exception as e:
        print(f"❌ Quick Apply ERROR: {e}")
    
    print("\n4. Testing Job Application (Custom Apply)")
    print("-" * 40)
    
    # Test custom apply
    custom_apply_data = {
        "job_id": job_id,
        "cover_letter": "I am very interested in this position.",
        "resume_url": "https://example.com/resume.pdf"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/applications/",
            json=custom_apply_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Custom Apply Status: {response.status_code}")
        print(f"Custom Apply Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ 422 UNPROCESSABLE CONTENT ERROR - Invalid request format")
            
    except Exception as e:
        print(f"❌ Custom Apply ERROR: {e}")

if __name__ == "__main__":
    job_id = test_endpoints()
    if job_id:
        test_job_application(job_id)
    
    print("\n" + "=" * 60)
    print("🎯 Debug test complete!")
