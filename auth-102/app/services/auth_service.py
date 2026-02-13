from datetime import timedelta
from typing import TYPE_CHECKING

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User
from app.schemas import Token, UserCreate

if TYPE_CHECKING:
    from sqlmodel import Session


def authenticate_user(session: "Session", username: str, password: str) -> User | None:
    """Authenticate a user by username and password."""
    from app.services.user_service import get_user_by_username

    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def register_user(session: "Session", user_create: UserCreate) -> User:
    """Register a new user with hashed password."""
    from app.services.user_service import get_user_by_username, get_user_by_email

    # Check if username already exists
    existing_user = get_user_by_username(session, user_create.username)
    if existing_user:
        raise ValueError("Username already registered")

    # Check if email already exists
    existing_email = get_user_by_email(session, user_create.email)
    if existing_email:
        raise ValueError("Email already registered")

    # Create new user with hashed password
    hashed_password = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_user_token(user: User) -> Token:
    """Create an access token for a user."""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}