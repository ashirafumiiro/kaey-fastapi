from fastapi import Depends, FastAPI
from pydantic import BaseModel

# from .dependencies import get_query_token, get_token_header
from .routers import items, users, auth
from .files import cloud


app = FastAPI(
    title="Kaey Website API",
    summary="A web api for serving the content on Kaey Ltd website",
    # dependencies=[Depends(get_query_token)]
    )


app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)


class APIMessage(BaseModel):
    message: str | None = None

@app.get("/", response_model=APIMessage, response_description='root path', description='Root Path')
async def root():
    return {"message": "Kaey Api Web App!"}
