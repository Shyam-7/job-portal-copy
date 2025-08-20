from fastapi.testclient import TestClient

def get_admin_auth_token(client: TestClient) -> str:
    client.post("/api/auth/register", json={"email": "admin_job@example.com", "password": "password", "name": "Admin Job User", "role": "admin"})
    response = client.post("/api/auth/login", data={"username": "admin_job@example.com", "password": "password"})
    return response.json()["access_token"]

def test_create_job(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/api/jobs/",
        headers=headers,
        json={"title": "Test Job", "company_name": "Test Company", "description": "A job for testing"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Job"
    assert "id" in data

def test_get_all_active_jobs(client: TestClient):
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_all_jobs_for_admin(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/jobs/admin/all", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_job_by_id(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a job to get
    response = client.post(
        "/api/jobs/",
        headers=headers,
        json={"title": "Job To Get", "company_name": "Get Company", "description": "A job for getting"}
    )
    job_id = response.json()["id"]

    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["title"] == "Job To Get"

def test_update_job(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a job to update
    response = client.post(
        "/api/jobs/",
        headers=headers,
        json={"title": "Job To Update", "company_name": "Update Company", "description": "A job for updating"}
    )
    job_id = response.json()["id"]

    response = client.put(
        f"/api/jobs/{job_id}",
        headers=headers,
        json={"title": "Updated Job Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Job Title"

def test_delete_job(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a job to delete
    response = client.post(
        "/api/jobs/",
        headers=headers,
        json={"title": "Job To Delete", "company_name": "Delete Company", "description": "A job for deleting"}
    )
    job_id = response.json()["id"]

    response = client.delete(f"/api/jobs/{job_id}", headers=headers)
    assert response.status_code == 200

    # Verify job is deleted
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 404

def test_filter_jobs_by_title(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Software Engineer", "company_name": "Tech Co", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Data Scientist", "company_name": "Data Inc", "description": "..."})

    response = client.get("/api/jobs/?title=Software")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Software Engineer"

def test_filter_jobs_by_location(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Backend Dev", "company_name": "Server Co", "location": "New York", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Frontend Dev", "company_name": "Client Co", "location": "San Francisco", "description": "..."})

    response = client.get("/api/jobs/?location=New York")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["location"] == "New York"

def test_sort_jobs_by_newest(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Job A", "company_name": "A Co", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Job B", "company_name": "B Co", "description": "..."})

    response = client.get("/api/jobs/?sort_by=newest")
    assert response.status_code == 200
    jobs = response.json()
    assert jobs[0]["title"] == "Job B"

def test_sort_jobs_by_oldest(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Job C", "company_name": "C Co", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Job D", "company_name": "D Co", "description": "..."})

    response = client.get("/api/jobs/?sort_by=oldest")
    assert response.status_code == 200
    jobs = response.json()
    assert jobs[0]["title"] == "Job C"

def test_filter_jobs_by_experience_level(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Senior Dev", "company_name": "Expert Co", "experience_level": "Senior", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Junior Dev", "company_name": "Beginner Co", "experience_level": "Junior", "description": "..."})

    response = client.get("/api/jobs/?experience_level=Senior")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["experience_level"] == "Senior"

def test_filter_jobs_by_salary_range(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "High Paying Job", "company_name": "Rich Co", "salary_min": 150000, "salary_max": 200000, "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Low Paying Job", "company_name": "Poor Co", "salary_min": 50000, "salary_max": 70000, "description": "..."})

    response = client.get("/api/jobs/?salary_min=100000")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "High Paying Job"

def test_filter_jobs_by_company_type(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Startup Job", "company_name": "Agile Co", "company_type": "Startup", "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Corporate Job", "company_name": "Big Co", "company_type": "Corporate", "description": "..."})

    response = client.get("/api/jobs/?company_type=Startup")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company_type"] == "Startup"

def test_filter_jobs_by_work_type(client: TestClient):
    token = get_admin_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/jobs/", headers=headers, json={"title": "Remote Job", "company_name": "Home Co", "is_remote": True, "description": "..."})
    client.post("/api/jobs/", headers=headers, json={"title": "Office Job", "company_name": "Office Co", "work_type": "On-site", "description": "..."})

    response = client.get("/api/jobs/?work_type=remote")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["is_remote"] == True
