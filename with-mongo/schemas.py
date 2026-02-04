from pydantic import BaseModel, Field, BeforeValidator, ConfigDict
from typing import Optional, Annotated

# This is a custom type for representing MongoDB's ObjectId in Pydantic models.
# It uses Pydantic's `Annotated` and `BeforeValidator` to ensure that the
# ObjectId is converted to a string for JSON serialization.
PyObjectId = Annotated[str, BeforeValidator(str)]

class ItemBase(BaseModel):
    """
    Base model for an item. Contains all the common attributes of an item.
    """
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemCreate(ItemBase):
    """
    Model for creating an item. Inherits from ItemBase.
    """
    pass

class Item(ItemBase):
    """
    Model for representing an item retrieved from the database.
    It includes the `id` field, which is the MongoDB `_id`.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
