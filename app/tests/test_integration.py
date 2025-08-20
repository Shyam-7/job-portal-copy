from fastapi.testclient import TestClient

def test_admin_job_creation_and_user_visibility(client: TestClient, admin_token: str, user_token: str):
    # Admin creates a job
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/jobs/",
        headers=admin_headers,
        json={"title": "Integration Test Job", "company_name": "Integration Inc", "description": "A job for integration testing"}
    )
    assert response.status_code == 201
    job = response.json()
    job_id = job["id"]

    # User can see the job
    user_headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/api/jobs/{job_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Integration Test Job"

    # Admin deactivates the job
    response = client.put(
        f"/api/jobs/{job_id}",
        headers=admin_headers,
        json={"status": "inactive"}
    )
    assert response.status_code == 200

    # User can no longer see the job in the main list
    response = client.get("/api/jobs/", headers=user_headers)
    assert response.status_code == 200
    assert not any(j["id"] == job_id for j in response.json())

def test_user_application_and_admin_visibility(client: TestClient, admin_token: str, user_token: str, job: dict):
    # User applies for a job
    user_headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]
    response = client.post(
        "/api/applications/",
        headers=user_headers,
        json={"job_id": job_id, "cover_letter": "Integration test application"}
    )
    assert response.status_code == 200
    application = response.json()
    application_id = application["id"]

    # Admin can see the application
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/applications/job/{job_id}", headers=admin_headers)
    assert response.status_code == 200
    assert any(a["id"] == application_id for a in response.json())

    # Admin updates the application status
    response = client.patch(
        f"/api/applications/{application_id}",
        headers=admin_headers,
        json={"status": "reviewed"}
    )
    assert response.status_code == 200

    # User can see the updated status
    response = client.get(f"/api/applications/{application_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "reviewed"
