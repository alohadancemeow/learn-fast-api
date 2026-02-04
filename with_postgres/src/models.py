from sqlalchemy import Column, Integer, String

from .database import Base


class Post(Base):
    """
    SQLAlchemy model for a Post.
    Represents the 'posts' table in the database.
    """
    __tablename__ = "posts"

    # Unique identifier for the post, also serving as the primary key.
    id = Column(Integer, primary_key=True, index=True)
    # Title of the post, indexed for efficient lookups.
    title = Column(String, index=True)
    # Full content of the post.
    content = Column(String)


class Item(Base):
    """
    SQLAlchemy model for an Item.
    Represents the 'items' table in the database.
    """
    __tablename__ = "items"

    # Unique identifier for the item, serving as the primary key.
    id = Column(Integer, primary_key=True, index=True)
    # Name of the item.
    name = Column(String, index=True)
    # Optional description of the item.
    description = Column(String, nullable=True)
    # Price of the item.
    price = Column(Integer) # Using Integer for simplicity, might be Float in real app
    # Optional tax percentage for the item.
    tax = Column(Integer, nullable=True) # Using Integer for simplicity