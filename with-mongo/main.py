from fastapi import FastAPI, HTTPException
from typing import List
from . import crud, schemas
from .database import client

app = FastAPI()


@app.post("/items/", response_model=schemas.Item)
def create_item_endpoint(item: schemas.ItemCreate):
    """
    Create a new item.
    """
    return crud.create_item(item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items_endpoint():
    """
    Retrieve all items.
    """
    return crud.get_items()


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item_endpoint(item_id: str):
    """
    Retrieve a single item by its ID.
    """
    item = crud.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item_endpoint(item_id: str, item: schemas.ItemCreate):
    """
    Update an existing item.
    """
    updated_item = crud.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@app.delete("/items/{item_id}", response_model=dict)
def delete_item_endpoint(item_id: str):
    """
    Delete an item.
    """
    if not crud.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@app.get("/health")
def health_check():
    """
    Check if the API and Database are running correctly.
    """
    try:
        # Check MongoDB connection
        client.admin.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not available: {str(e)}")
