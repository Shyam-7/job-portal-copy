from fastapi.testclient import TestClient

def test_apply_for_job(client: TestClient, user_token: str, job: dict):
    headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]

    response = client.post(
        "/api/applications/",
        headers=headers,
        json={"job_id": job_id, "cover_letter": "I am a great candidate!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert data["cover_letter"] == "I am a great candidate!"

def test_get_my_applications(client: TestClient, user_token: str):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/applications/me", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_application_by_id(client: TestClient, user_token: str, job: dict):
    user_headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]

    response = client.post(
        "/api/applications/",
        headers=user_headers,
        json={"job_id": job_id, "cover_letter": "I want to be seen"}
    )
    application_id = response.json()["id"]

    response = client.get(f"/api/applications/{application_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["id"] == application_id

def test_get_applications_for_job_as_admin(client: TestClient, admin_token: str, job: dict):
    job_id = job["id"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get(f"/api/applications/job/{job_id}", headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_application_status_as_admin(client: TestClient, admin_token: str, user_token: str, job: dict):
    job_id = job["id"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    response = client.post(
        "/api/applications/",
        headers=user_headers,
        json={"job_id": job_id, "cover_letter": "Please review my application"}
    )
    application_id = response.json()["id"]

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.patch(
        f"/api/applications/{application_id}",
        headers=admin_headers,
        json={"status": "reviewed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "reviewed"

def test_withdraw_application(client: TestClient, user_token: str, job: dict):
    job_id = job["id"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    response = client.post(
        "/api/applications/",
        headers=user_headers,
        json={"job_id": job_id, "cover_letter": "I want to withdraw this"}
    )
    application_id = response.json()["id"]

    response = client.delete(f"/api/applications/{application_id}", headers=user_headers)
    assert response.status_code == 200

    # Verify application is deleted
    response = client.get(f"/api/applications/{application_id}", headers=user_headers)
    assert response.status_code == 404 # Not Found
