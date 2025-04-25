import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base, get_db
from app.models.users import User
from app.core.security import get_password_hash

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Apply mocks to bypass Neo4j connections
@pytest.fixture(scope="module", autouse=True)
def mock_neo4j():
    # Create mock for Neo4jDatabase class
    neo4j_db_mock = MagicMock()
    neo4j_db_mock.get_driver.return_value = MagicMock()
    neo4j_db_mock.verify_curriculum_structure.return_value = True
    neo4j_db_mock.create_curriculum_structure.return_value = None
    
    # Patch the neo4j_db instance and init function
    with patch("app.db.neo4j.neo4j_db", neo4j_db_mock):
        with patch("app.db.neo4j.init_neo4j_db") as mock_init:
            mock_init.return_value = None
            yield


@pytest.fixture(scope="module")
def test_db():
    # Create the test database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test user
    db = TestingSessionLocal()
    test_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(test_user)
    db.commit()
    db.close()
    
    yield  # Run the tests
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    with TestClient(app) as c:
        yield c


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "grade_level": 8
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_username(client):
    # First registration
    response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicate",
            "email": "first@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    
    # Duplicate username
    response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicate",
            "email": "second@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_login_user(client):
    # Login with correct credentials
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_json(client):
    # Login using JSON endpoint
    response = client.post(
        "/api/auth/login-json",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data
    assert data["token_type"] == "bearer"


def test_get_user_profile(client):
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "password123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get user profile with token
    response = client.get(
        "/api/auth/user",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "testuser"
    assert user_data["email"] == "test@example.com"


def test_get_user_profile_no_token(client):
    # Try to get user profile without token
    response = client.get("/api/auth/user")
    assert response.status_code == 401