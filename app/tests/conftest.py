import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.config import settings
import os
from app.api.deps import get_db

# Set environment to testing
os.environ['TESTING'] = 'True'

SQLALCHEMY_DATABASE_URL = settings.test_database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    A fixture that provides a test client for the FastAPI application.
    It handles database setup and teardown for each test function.
    """
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass # The db_session fixture will handle closing

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up dependency overrides
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_token(client: TestClient) -> str:
    """
    A fixture that provides an admin token for the tests.
    It creates an admin user and logs in to get the token.
    """
    email = "test_admin@example.com"
    password = "adminpassword"

    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Test Admin", "role": "admin"})
    response = client.post("/api/auth/login", data={"username": email, "password": password})

    return response.json()["access_token"]

@pytest.fixture(scope="function")
def user_token(client: TestClient) -> str:
    """
    A fixture that provides a regular user token for the tests.
    """
    email = "test_user@example.com"
    password = "userpassword"

    client.post("/api/auth/register", json={"email": email, "password": password, "name": "Test User", "role": "user"})
    response = client.post("/api/auth/login", data={"username": email, "password": password})

    return response.json()["access_token"]

from jose import jwt
from app.config import settings

@pytest.fixture(scope="function")
def job(client: TestClient, admin_token: str) -> dict:
    """
    A fixture that creates a job for the tests.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post(
        "/api/jobs/",
        headers=headers,
        json={"title": "Test Job for Applications", "company_name": "Test Co", "description": "A job for testing applications"}
    )
    return response.json()

def decode_token(token: str) -> str:
    """
    Decodes a JWT token and returns the user ID (sub).
    """
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload.get("sub")
