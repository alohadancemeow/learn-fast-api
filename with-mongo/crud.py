# from pymongo.collection import Collection
from bson import ObjectId
from . import schemas
from .database import get_collection

def create_item(item: schemas.ItemCreate) -> schemas.Item:
    """
    Create a new item in the database.

    Args:
        item: The item to create, based on the ItemCreate schema.

    Returns:
        The created item, based on the Item schema.
    """
    collection = get_collection()
    item_dict = item.dict()
    inserted_id = collection.insert_one(item_dict).inserted_id
    created_item = collection.find_one({"_id": inserted_id})
    return schemas.Item(**created_item)

def get_item(item_id: str) -> schemas.Item:
    """
    Retrieve a single item from the database by its ID.

    Args:
        item_id: The ID of the item to retrieve.

    Returns:
        The retrieved item, or None if not found.
    """
    collection = get_collection()
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return schemas.Item(**item)
    return None

def get_items() -> list[schemas.Item]:
    """
    Retrieve all items from the database.

    Returns:
        A list of all items.
    """
    collection = get_collection()
    items = []
    for item in collection.find():
        items.append(schemas.Item(**item))
    return items

def update_item(item_id: str, item: schemas.ItemCreate) -> schemas.Item:
    """
    Update an existing item in the database.

    Args:
        item_id: The ID of the item to update.
        item: The new data for the item.

    Returns:
        The updated item.
    """
    collection = get_collection()
    collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    updated_item = get_item(item_id)
    return updated_item

def delete_item(item_id: str) -> bool:
    """
    Delete an item from the database.

    Args:
        item_id: The ID of the item to delete.

    Returns:
        True if the item was deleted, False otherwise.
    """
    collection = get_collection()
    result = collection.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count > 0
