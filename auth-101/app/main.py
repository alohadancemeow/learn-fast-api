# app/main.py

"""
This is the main entry point of the FastAPI application.

It creates the FastAPI app instance, includes the API routers,
and defines the startup and shutdown event handlers.
"""

from fastapi import FastAPI
from .database import database, engine, metadata
from .routers import todos, users

# Create all tables
metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Include API routers
app.include_router(users.router, tags=["users"])
app.include_router(todos.router, tags=["todos"])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
