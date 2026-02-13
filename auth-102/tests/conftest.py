import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_session
from app.main import app
from app.models import User

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    """Override database session for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Fixture for a test database session."""
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture for a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Fixture for a test user in the database."""
    from app.core.security import get_password_hash

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_token(test_user, client):
    """Fixture for a valid access token for test_user."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    return response.json()["access_token"]