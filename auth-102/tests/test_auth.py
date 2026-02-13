def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "password" not in data  # Password should not be in response


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",  # Already exists
            "email": "different@example.com",
            "password": "securepass123"
        }
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "different",
            "email": "test@example.com",  # Already exists
            "password": "securepass123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_username(client, test_user):
    """Test login with invalid username."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wronguser", "password": "testpass123"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_invalid_password(client, test_user):
    """Test login with invalid password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_token_protected_endpoint(client, test_token):
    """Test accessing a protected endpoint with valid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_protected_endpoint_without_token(client):
    """Test accessing a protected endpoint without token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_protected_endpoint_invalid_token(client):
    """Test accessing a protected endpoint with invalid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401