# app/database.py

"""
This module handles the database connection and SQLAlchemy setup.

It defines:
- The database URL.
- The `Database` object for executing queries.
- The SQLAlchemy `MetaData` object.
- The table definitions for `users` and `todos`.
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey
from databases import Database

from ..core.config import settings

# Database configuration
DATABASE_URL = settings.DATABASE_URL
database = Database(DATABASE_URL)
metadata = MetaData()

# SQLAlchemy table definitions for Users and Todos
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("disabled", Boolean, default=False),
)

todos_table = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String),
    Column("description", String, nullable=True),
    Column("completed", Boolean, default=False),
    Column("owner_id", Integer, ForeignKey("users.id")),
)

# Create an engine instance for the startup event to create tables.
# This is a synchronous engine, so it should be used carefully in async context.
engine = create_engine(DATABASE_URL)
