from fastapi.testclient import TestClient

def get_auth_token(client: TestClient, admin=False) -> str:
    email = "admin@example.com" if admin else "test@example.com"
    password = "password123"
    name = "Admin User" if admin else "Test User"
    role = "admin" if admin else "user"

    client.post("/api/auth/register", json={"email": email, "password": password, "name": name, "role": role})
    response = client.post("/api/auth/login", data={"username": email, "password": password})

    if response.status_code != 200:
        # try to register again if login fails, user might exist from previous tests
        client.post("/api/auth/register", json={"email": email, "password": password, "name": name, "role": role})
        response = client.post("/api/auth/login", data={"username": email, "password": password})

    return response.json()["access_token"]

def test_get_user_profile(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/users/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"

def test_update_user_profile(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.patch("/api/users/profile", headers=headers, json={"headline": "New Headline"})
    assert response.status_code == 200
    data = response.json()
    assert data["headline"] == "New Headline"

def test_get_all_users_as_admin(client: TestClient):
    admin_token = get_auth_token(client, admin=True)
    headers = {"Authorization": f"Bearer {admin_token}"}

    get_auth_token(client)

    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_user_by_id_as_admin(client: TestClient):
    admin_token = get_auth_token(client, admin=True)
    headers = {"Authorization": f"Bearer {admin_token}"}

    admin_profile_response = client.get("/api/users/profile", headers=headers)
    admin_id = admin_profile_response.json()["user"]["id"]

    response = client.get(f"/api/users/{admin_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == admin_id

def test_update_user_status_as_admin(client: TestClient):
    admin_token = get_auth_token(client, admin=True)
    headers = {"Authorization": f"Bearer {admin_token}"}

    get_auth_token(client)
    users_response = client.get("/api/users/", headers=headers)
    regular_user = next((u for u in users_response.json() if u["role"] == "user"), None)
    assert regular_user is not None

    user_id = regular_user["id"]

    response = client.patch(f"/api/users/{user_id}/status", headers=headers, json={"status": "inactive"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "inactive"

def test_delete_user_as_admin(client: TestClient):
    admin_token = get_auth_token(client, admin=True)
    headers = {"Authorization": f"Bearer {admin_token}"}

    client.post("/api/auth/register", json={"email": "delete@me.com", "password": "password", "name": "Delete Me"})

    users_response = client.get("/api/users/", headers=headers)
    user_to_delete = next((u for u in users_response.json() if u["email"] == "delete@me.com"), None)
    assert user_to_delete is not None

    user_id = user_to_delete["id"]

    response = client.delete(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 404

def test_get_user_profile_after_creation(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/users/profile", headers=headers)
    assert response.status_code == 200
    profile = response.json()
    assert profile["headline"] is None

def test_update_user_profile_fields(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    update_data = {
        "headline": "Software Engineer",
        "location": "San Francisco",
        "about": "I am a software engineer."
    }

    response = client.patch("/api/users/profile", headers=headers, json=update_data)
    assert response.status_code == 200
    profile = response.json()
    assert profile["headline"] == "Software Engineer"
    assert profile["location"] == "San Francisco"
    assert profile["about"] == "I am a software engineer."

def test_upload_resume(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    with open("test_resume.txt", "w") as f:
        f.write("This is a test resume.")

    with open("test_resume.txt", "rb") as f:
        response = client.post("/api/users/profile/resume", headers=headers, files={"file": f})

    assert response.status_code == 200
    profile = response.json()
    assert profile["resume_url"] is not None
    assert "resumes/" in profile["resume_url"]
    assert ".txt" in profile["resume_url"]

def test_get_all_users_as_non_admin(client: TestClient):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 403
