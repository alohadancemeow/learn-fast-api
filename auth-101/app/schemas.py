# app/schemas.py

"""
This module defines the Pydantic models for data validation and serialization.

It includes schemas for:
- Todos: TodoBase, TodoCreate, Todo
- Users: UserBase, UserCreate, User, UserInDB
"""

from pydantic import BaseModel
from typing import Optional

# Pydantic models for Todo
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    owner_id: Optional[int] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# Pydantic models for User
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
