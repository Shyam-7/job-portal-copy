from fastapi.testclient import TestClient

def test_save_and_get_saved_jobs(client: TestClient, user_token: str, job: dict):
    headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]

    # Save a job
    response = client.post(f"/api/saved-jobs/{job_id}", headers=headers)
    assert response.status_code == 200

    # Get saved jobs
    response = client.get("/api/saved-jobs/", headers=headers)
    assert response.status_code == 200
    saved_jobs = response.json()
    assert len(saved_jobs) > 0
    assert any(sj["job_id"] == job_id for sj in saved_jobs)

def test_unsave_job(client: TestClient, user_token: str, job: dict):
    headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]

    # Save a job first
    client.post(f"/api/saved-jobs/{job_id}", headers=headers)

    # Unsave the job
    response = client.delete(f"/api/saved-jobs/{job_id}", headers=headers)
    assert response.status_code == 200

    # Verify job is unsaved
    response = client.get("/api/saved-jobs/", headers=headers)
    assert not any(sj["job_id"] == job_id for sj in response.json())

def test_save_already_saved_job(client: TestClient, user_token: str, job: dict):
    headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]

    # Save a job twice
    client.post(f"/api/saved-jobs/{job_id}", headers=headers)
    response = client.post(f"/api/saved-jobs/{job_id}", headers=headers)

    assert response.status_code == 400
