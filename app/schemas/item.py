from typing import Optional, Annotated
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class ItemBase(BaseModel):
    label: str
    description: str | None = None
    amount: str | None = None
    category: str
    image: str

class Item(ItemBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class ItemIn(ItemBase):
    pass
    


class ItemsCollection(BaseModel):
    items : list[Item]


class UpdateItem(BaseModel):
    label: str | None = None
    description: str | None = None
    amount: str | None = None
    category: str | None = None