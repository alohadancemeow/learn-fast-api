"""
Pydantic Schemas

This module defines the Pydantic models used for data validation and serialization
in the API. These schemas ensure that incoming requests contain valid data and
that outgoing responses are formatted correctly.

- Base models (e.g., PostBase, ItemBase) define shared attributes.
- Create models (e.g., PostCreate, ItemCreate) are used for creating new resources.
- Response models (e.g., PostResponse, ItemResponse) include system-generated fields like IDs.
"""

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    tax: float | None = Field(None, ge=0, le=100, description="Tax percentage (0-100)")


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int  # Assuming items will also have an ID from the database

    model_config = ConfigDict(from_attributes=True)
