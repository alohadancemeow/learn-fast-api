from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Define the data model for an Item using Pydantic
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory database (list of Item objects)
db = []

# --- CRUD Operations ---

# Create operation: Add a new item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    db.append(item)
    return item

# Read all items operation
@app.get("/items/", response_model=List[Item])
def read_items():
    return db

# Read a single item by its ID (index in the list)
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# Update operation: Modify an existing item by its ID
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return item

# Delete operation: Remove an item by its ID
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    return db.pop(item_id)
