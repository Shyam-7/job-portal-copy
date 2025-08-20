from fastapi.testclient import TestClient

def test_register(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpassword", "name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login(client: TestClient):
    # First, register a user
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpassword", "name": "Test User"},
    )
    # Then, login
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_forgot_password(client: TestClient):
    # Register a user first
    email = "forgot@example.com"
    password = "password"
    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Forgot"})

    response = client.post("/api/auth/forgot-password", json={"email": email})
    assert response.status_code == 200
    assert "token" in response.json()

def test_reset_password(client: TestClient):
    # Register a user and get a reset token
    email = "reset@example.com"
    password = "password"
    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Reset"})
    response = client.post("/api/auth/forgot-password", json={"email": email})
    token = response.json()["token"]

    # Reset the password
    new_password = "newpassword"
    response = client.post("/api/auth/reset-password", json={"token": token, "new_password": new_password})
    assert response.status_code == 200

    # Try to log in with the new password
    response = client.post("/api/auth/login", data={"username": email, "password": new_password})
    assert response.status_code == 200

def test_register_existing_email(client: TestClient):
    email = "existing@example.com"
    password = "password"
    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Existing"})

    response = client.post("/api/auth/register", json={"email": email, "password": "password", "name": "Existing"})
    assert response.status_code == 400

def test_login_incorrect_password(client: TestClient):
    email = "incorrect@example.com"
    password = "password"
    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Incorrect"})

    response = client.post("/api/auth/login", data={"username": email, "password": "wrongpassword"})
    assert response.status_code == 401

def test_change_password(client: TestClient):
    # Register and log in a user
    email = "change@example.com"
    password = "password"
    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Change"})
    response = client.post("/api/auth/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Change the password
    new_password = "newpassword"
    response = client.post("/api/auth/change-password", headers=headers, json={"current_password": password, "new_password": new_password})
    assert response.status_code == 200

    # Try to log in with the new password
    response = client.post("/api/auth/login", data={"username": email, "password": new_password})
    assert response.status_code == 200
