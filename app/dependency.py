from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from dotenv import load_dotenv
from jose import jwt, JWTError
import os
from bson import ObjectId

from .schemas.token import Token, TokenData
from .schemas.user import User, UserInDB
from .db.client import db


load_dotenv()

users_collection = db.get_collection("users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(email: str | None):
    user = await users_collection.find_one({"email": email})
    if(user) is not None:
        return UserInDB(**user)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.enabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user