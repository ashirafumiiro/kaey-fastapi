from fastapi import APIRouter, Depends, HTTPException
from app.db.client import db
from bson import ObjectId
from typing import Annotated
from fastapi import Body, status, Response
from pymongo import ReturnDocument

from ..schemas.user import UserIn, User, UserBase, UpdateUser
from ..utils import get_password_hash
from ..dependency import get_current_active_user

collection = db.get_collection('users')

router = APIRouter(
    prefix="/users",
    tags=["User"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post(
  "/",
  response_model_by_alias=False,
  response_model=UserBase,
  dependencies=[Depends(get_current_active_user)])
async def create_user(user: Annotated[UserIn, Body()]):
    user_details = user.model_dump(by_alias=True, exclude=["password"])
    password_hash = get_password_hash(user.password)
    user_details.update({'hashed_password': password_hash, "enabled": True}) # disabled by default
    new_user = await collection.insert_one(user_details)
    created_student = await collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_student

@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@router.put(
    "/{id}",
    responses={403: {"description": "Operation forbidden"}},
    response_model_by_alias=False,
    dependencies=[Depends(get_current_active_user)]
)
async def update_item(id: str, user: Annotated[UpdateUser, Body()]):
    update_object = {k: v for k, v in user.model_dump(by_alias=True).items() if v is not None}
    update_result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_object},
            return_document=ReturnDocument.AFTER,
        )
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")