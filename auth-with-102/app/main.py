from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.database import init_db

# Initialize FastAPI app
app = FastAPI(title="FastAPI Authentication App", version="1.0.0")

# Include API routers
app.include_router(api_router)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "FastAPI Authentication App",
        "docs": "/docs",
        "endpoints": {
            "register": "POST /api/v1/auth/register",
            "login": "POST /api/v1/auth/login",
            "current_user": "GET /api/v1/users/me",
            "list_users": "GET /api/v1/users/"
        }
    }