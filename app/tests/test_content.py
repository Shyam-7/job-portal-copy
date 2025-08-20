from fastapi.testclient import TestClient

def test_get_public_content(client: TestClient):
    response = client.get("/api/content/public/user-dashboard")
    assert response.status_code == 200
    assert "hero" in response.json()

def test_create_and_get_content(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create content
    response = client.post(
        "/api/content/admin",
        headers=headers,
        json={"title": "About Us", "content": "We are a great company!", "section": "about", "section_type": "page"}
    )
    assert response.status_code == 200
    content = response.json()
    content_id = content["id"]

    # Get all content
    response = client.get("/api/content/admin", headers=headers)
    assert response.status_code == 200
    assert any(c["id"] == content_id for c in response.json())

    # Update content
    response = client.put(
        f"/api/content/admin/{content_id}",
        headers=headers,
        json={"content": "We are an even better company!"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "We are an even better company!"

    # Delete content
    response = client.delete(f"/api/content/admin/{content_id}", headers=headers)
    assert response.status_code == 200

    # Verify content is deleted
    response = client.get("/api/content/admin", headers=headers)
    assert not any(c["id"] == content_id for c in response.json())
