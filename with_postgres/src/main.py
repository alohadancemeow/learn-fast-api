from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import models
from .crud import create_item, create_post, delete_item, get_item, get_items, get_posts, update_item  # Import Item CRUD
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

from .schemas import ItemBase, ItemCreate, ItemResponse, PostCreate, PostResponse  # Import Item schemas  # noqa: E402

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    # This function is executed when the FastAPI application starts up.
    # It can be used to initialize database connections, load models, or perform other startup tasks.
    print("Connecting to database...")


@app.on_event("shutdown")
async def shutdown_db_client():
    # This function is executed when the FastAPI application shuts down.
    # It ensures that database connections are properly closed to prevent resource leaks.
    # SQLAlchemy manages connection pooling, so explicit engine disposal is often not strictly necessary
    # for simple cases but can be added for explicit control or complex scenarios.
    print("Disconnecting from database...")


class CustomError(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError):
    """
    Custom exception handler example
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error occurred: {exc.name}"},
    )


# --- API Endpoints ---


@app.post("/posts/", response_model=PostResponse)
def create_post_endpoint(post: PostCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new post.
    Delegates to the crud module for database interaction.
    """
    return create_post(db=db, post=post)


@app.get("/posts/", response_model=list[PostResponse])
def read_posts_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    API endpoint to retrieve a list of posts.
    Delegates to the crud module for database interaction with pagination.
    """
    return get_posts(db=db, skip=skip, limit=limit)


@app.post("/items/", response_model=ItemResponse)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new item.
    Delegates to the crud module for database interaction.
    """
    return create_item(db=db, item=item)


@app.get("/items/", response_model=list[ItemResponse])
def read_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    API endpoint to retrieve a list of items.
    Delegates to the crud module for database interaction with pagination.
    """
    return get_items(db=db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to retrieve a single item by ID.
    Delegates to the crud module for database interaction.
    """
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item_endpoint(item_id: int, item: ItemBase, db: Session = Depends(get_db)):
    """
    API endpoint to update an existing item.
    Delegates to the crud module for database interaction.
    """
    db_item = update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to delete an item.
    Delegates to the crud module for database interaction.
    """
    db_item = delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@app.get("/error-example")
async def error_example(*, trigger_error: bool = False):
    """
    Example endpoint that can trigger custom exception
    """
    if trigger_error:
        msg = "example error"
        raise CustomError(msg)
    return {"message": "No error occurred"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint with timestamp
    """
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}
