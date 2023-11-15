from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from typing import Annotated
from fastapi import File, Form, UploadFile, Path, Body, status, Response
import cloudinary
import cloudinary.uploader
from pymongo import ReturnDocument


from app.db.client import db
from app.schemas.item import Item, ItemsCollection, ItemIn, UpdateItem
from ..schemas.user import User
from ..dependency import get_current_active_user

collection = db.get_collection('items')

router = APIRouter(
    prefix="/store",
    tags=["Store"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", 
    response_model=ItemsCollection,
    response_model_by_alias=False)
async def read_items():
    try:
        items = await collection.find().to_list(1000)
        return ItemsCollection(items=items)
    except:
        raise HTTPException(status_code=500, detail="An error occured")


@router.get(
    "/{id}", 
    response_model=Item,
    response_model_by_alias=False)
async def read_item(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    student = await collection.find_one({"_id": ObjectId(id)})
    if (student) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")



@router.put(
    "/{id}",
    responses={403: {"description": "Operation forbidden"}},
    response_model_by_alias=False,
    dependencies=[Depends(get_current_active_user)]
)
async def update_item(id: str, item: Annotated[UpdateItem, Body()]):
    update_object = {k: v for k, v in item.model_dump(by_alias=True).items() if v is not None}
    update_result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_object},
            return_document=ReturnDocument.AFTER,
        )
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.post(
    "/",
    response_description="Add new student",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_active_user)]
    )
async def create_item(
    file: Annotated[UploadFile, File()],
    label: Annotated[str, Form()],
    category: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    amount: Annotated[str | None, Form()] = None,
    ):

    new_item = await collection.insert_one(
        {"lable": label, "description": description, "amount": amount, "catetory": category}
    )
    inserted_id = new_item.inserted_id

    result = cloudinary.uploader.upload(file.file)
    url = result.get('url')

    update_result = await collection.find_one_and_update(
            {"_id": ObjectId(inserted_id)},
            {"$set": {"image": url}},
            return_document=ReturnDocument.AFTER,
        )
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=500, detail=f"Failed to add image")


@router.post(
    "/{id}/image-update", 
    response_model=Item,
    response_model_by_alias=False,
    dependencies=[Depends(get_current_active_user)]
    )
async def update_item_image(
    file: Annotated[UploadFile, File()],
    id: str, 
    ):

    result = cloudinary.uploader.upload(file.file)
    url = result.get('url')

    update_result = await collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {"image": url}},
            return_document=ReturnDocument.AFTER,
        )
    if update_result is not None:
        return update_result
    else:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")


# todo: delete images from cloudinary   
@router.delete("/students/{id}", response_description="Delete a student", dependencies=[Depends(get_current_active_user)])
async def delete_student(id: str):
    """
    Remove a single Item record from the database.
    """
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")