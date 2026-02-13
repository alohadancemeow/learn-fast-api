from fastapi import APIRouter

from app.api.v1.endpoints import auth, users

api_router = APIRouter(prefix="/api/v1")

# Include auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include user endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])