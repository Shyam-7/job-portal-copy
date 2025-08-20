from fastapi.testclient import TestClient
from .conftest import decode_token

def test_create_and_get_messages(client: TestClient, user_token: str, admin_token: str, job: dict):
    # Create an application to send messages about
    user_headers = {"Authorization": f"Bearer {user_token}"}
    job_id = job["id"]
    response = client.post(
        "/api/applications/",
        headers=user_headers,
        json={"job_id": job_id, "cover_letter": "Message test application"}
    )
    application_id = response.json()["id"]

    # User sends a message to admin
    admin_id = decode_token(admin_token)
    response = client.post(
        "/api/communication/messages",
        headers=user_headers,
        json={"application_id": application_id, "recipient_id": admin_id, "content": "Hello Admin!"}
    )
    assert response.status_code == 201

    # Admin sends a message to user
    user_id = decode_token(user_token)
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/communication/messages",
        headers=admin_headers,
        json={"application_id": application_id, "recipient_id": user_id, "content": "Hello User!"}
    )
    assert response.status_code == 201

    # Get messages for the application
    response = client.get(f"/api/communication/{application_id}/messages", headers=user_headers)
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2

def test_unauthorized_message_access(client: TestClient, job: dict, user_token: str):
    # user_token is user 1

    # Create a second user
    email2 = "user2@example.com"
    password2 = "password"
    client.post("/api/auth/register", json={"email": email2, "password": password2, "name": "User 2", "role": "user"})
    user2_token = client.post("/api/auth/login", data={"username": email2, "password": password2}).json()["access_token"]

    # User 1 applies for a job
    user1_headers = {"Authorization": f"Bearer {user_token}"}
    response = client.post("/api/applications/", headers=user1_headers, json={"job_id": job["id"], "cover_letter": "User 1 application"})
    application_id = response.json()["id"]

    # User 2 tries to access messages for user 1's application
    user2_headers = {"Authorization": f"Bearer {user2_token}"}
    response = client.get(f"/api/communication/{application_id}/messages", headers=user2_headers)
    assert response.status_code == 403

def test_get_announcement_stats(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create some announcements
    client.post("/api/communication/announcements", headers=headers, json={"title": "Draft announcement", "content": "...", "status": "draft"})
    client.post("/api/communication/announcements", headers=headers, json={"title": "Scheduled announcement", "content": "...", "status": "scheduled"})
    client.post("/api/communication/announcements", headers=headers, json={"title": "Sent announcement", "content": "...", "status": "sent"})

    response = client.get("/api/communication/announcements/stats", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] >= 3
    assert stats["draft"] >= 1
    assert stats["scheduled"] >= 1
    assert stats["sent"] >= 1

def test_get_scheduled_announcements(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.post("/api/communication/announcements", headers=headers, json={"title": "Scheduled for test", "content": "...", "status": "scheduled"})

    response = client.get("/api/communication/announcements/scheduled", headers=headers)
    assert response.status_code == 200
    announcements = response.json()
    assert len(announcements) > 0
    assert announcements[0]["status"] == "scheduled"

def test_get_draft_announcements(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}
    client.post("/api/communication/announcements", headers=headers, json={"title": "Draft for test", "content": "...", "status": "draft"})

    response = client.get("/api/communication/announcements/drafts", headers=headers)
    assert response.status_code == 200
    announcements = response.json()
    assert len(announcements) > 0
    assert announcements[0]["status"] == "draft"

def test_send_custom_notification(client: TestClient, admin_token: str, user_token: str):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_id = decode_token(user_token)

    response = client.post(
        f"/api/communication/notifications/send?user_id={user_id}&title=Custom&message=Hello",
        headers=admin_headers
    )
    assert response.status_code == 200
    notification = response.json()
    assert notification["title"] == "Custom"

    # Verify user received the notification
    user_headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/communication/notifications", headers=user_headers)
    notifications = response.json()
    assert any(n["id"] == notification["id"] for n in notifications)
