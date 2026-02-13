from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models import User
from app.schemas import UserResponse
from app.services import user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the current authenticated user's profile.
    """
    return current_user


@router.get("/", response_model=List[UserResponse])
def list_users(current_user: Annotated[User, Depends(get_current_user)], session=Depends(get_session)):
    """
    List all users (requires authentication).

    This endpoint can be modified to require admin privileges.
    """
    return user_service.list_all_users(session)