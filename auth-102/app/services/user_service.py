from typing import List, TYPE_CHECKING

from app.models import User

if TYPE_CHECKING:
    from sqlmodel import Session


def get_user_by_username(session: "Session", username: str) -> User | None:
    """Get a user by username."""
    return session.query(User).where(User.username == username).first()


def get_user_by_email(session: "Session", email: str) -> User | None:
    """Get a user by email."""
    return session.query(User).where(User.email == email).first()


def list_all_users(session: "Session") -> List[User]:
    """List all users in the database."""
    return session.query(User).all()