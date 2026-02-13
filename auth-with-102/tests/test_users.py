def test_get_current_user(client, test_token, test_user):
    """Test getting current user profile."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id


def test_list_users(client, test_token, test_user):
    """Test listing all users."""
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert any(u["username"] == "testuser" for u in users)


def test_list_multiple_users(client, db_session, test_token):
    """Test listing multiple users."""
    from app.core.security import get_password_hash
    from app.models import User

    # Add another user
    user2 = User(
        username="user2",
        email="user2@example.com",
        hashed_password=get_password_hash("pass123"),
        is_active=True
    )
    db_session.add(user2)
    db_session.commit()

    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 2
    usernames = [u["username"] for u in users]
    assert "testuser" in usernames
    assert "user2" in usernames