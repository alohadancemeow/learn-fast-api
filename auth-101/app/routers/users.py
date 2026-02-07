# app/routers/users.py

"""
This module defines the API routes for user management and authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core import schemas, crud
from ..security import auth

router = APIRouter()


"""
Registers a new user in the system.

This endpoint takes a username and password, hashes the password for security,
and stores the new user in the database.

Args:
    user_create (schemas.UserCreate): The user data to register (username and password).

Returns:
    schemas.User: The newly created user object (excluding the password).

Raises:
    HTTPException (400): If the username is already taken.
"""


@router.post(
    "/register/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
async def register_user(user_create: schemas.UserCreate):
    db_user = await crud.get_user(username=user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return await crud.create_user(user=user_create)


"""
Authenticates a user and issues an access token.

This endpoint verifies the provided username and password against the database.
If valid, it returns a JWT access token that can be used for authenticated requests.
FastAPI's OAuth2PasswordRequestForm dependency handles the form data parsing.

Args:
    form_data (OAuth2PasswordRequestForm): Contains the username and password submitted by the user.

Returns:
    dict: A dictionary containing the access token and its type ("bearer").

Raises:
    HTTPException (401): If authentication fails (incorrect username or password).
"""


@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


"""
Retrieves the currently authenticated user's profile.

This endpoint uses the `get_current_user` dependency to validate the JWT token
from the request header and return the associated user object.

Args:
    current_user (schemas.User): The authenticated user object injected by the dependency.

Returns:
    schemas.User: The current user's profile information.
"""


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user
