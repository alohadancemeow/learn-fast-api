from sqlalchemy.orm import Session

from .models import Item, Post  # Added Item
from .schemas import ItemBase, ItemCreate, PostCreate  # Added ItemCreate, ItemBase (for update)


def create_post(db: Session, post: PostCreate):
    """
    Creates a new post in the database.
    This function takes a PostCreate schema, converts it to a Post ORM model,
    adds it to the session, commits the transaction, and refreshes the object
    to load any database-generated fields (like the ID).
    """
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of posts from the database with optional pagination.
    This function queries the database for Post objects, applying an offset
    and limit for pagination, and returns the results.
    """
    return db.query(Post).offset(skip).limit(limit).all()

# --- Item CRUD Operations ---

def create_item(db: Session, item: ItemCreate):
    """
    Creates a new item in the database.
    """
    db_item = Item(name=item.name, description=item.description, price=item.price, tax=item.tax)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    """
    Retrieves a single item by its ID.
    """
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of items with optional pagination.
    """
    return db.query(Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item: ItemBase):
    """
    Updates an existing item in the database.
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    """
    Deletes an item from the database.
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item