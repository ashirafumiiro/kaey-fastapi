from typing import Optional, Annotated
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserBase(BaseModel):
    name: str | None = None
    email: str
    enabled: bool | None = Field(default=False)

class UserIn(UserBase):
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    

class UserInDB(User):
    hashed_password: str


class UpdateUser(BaseModel):
    name: str | None = None
    email: str | None = None
    enabled: bool | None = None 