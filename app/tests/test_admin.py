from fastapi.testclient import TestClient

def test_get_admin_dashboard_stats(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/dashboard/stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert "totalUsers" in stats
    assert "totalJobs" in stats
    assert "totalApplications" in stats
    assert "pendingApplications" in stats
    assert "scheduledInterviews" in stats
    assert "activeJobs" in stats
    assert stats["totalUsers"] >= 1

def test_get_recent_jobs(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/dashboard/recent-jobs", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_recent_activity(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/admin/dashboard/recent-activity", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_analytics_overview(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/overview", headers=headers)
    assert response.status_code == 200
    overview = response.json()
    assert "totalUsers" in overview
    assert "totalJobs" in overview
    assert "totalApplications" in overview
    assert "activeJobs" in overview

def test_get_monthly_trends(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/monthly-trends", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_conversion_data(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/conversion", headers=headers)
    assert response.status_code == 200
    assert "totalVisits" in response.json()

def test_get_top_jobs(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/top-jobs", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_activity(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/user-activity", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_export_report(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/api/analytics/export/pdf", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()

def test_refresh_data(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post("/api/analytics/refresh", headers=headers)
    assert response.status_code == 200
    assert "message" in response.json()
