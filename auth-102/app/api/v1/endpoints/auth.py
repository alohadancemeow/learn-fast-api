from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db
from app.core.config import settings
from app.core.database import get_session
from app.core.security import create_access_token
from app.schemas import Token, UserCreate, UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session=Depends(get_session)):
    """
    Register a new user.

    - **username**: Unique username for the user
    - **email**: Unique email address
    - **password**: Plain text password (will be hashed)
    """
    try:
        user = auth_service.register_user(session, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_session)
):
    """
    Login with username and password to get an access token.
    """
    user = auth_service.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_user_token(user)