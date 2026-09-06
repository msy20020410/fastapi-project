from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.schemas.user import LoginUser, get_current_user, fake_users_db, UserInDB, fake_hash_password

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: Annotated[LoginUser, Depends(get_current_user)]):
    return current_user


class FormData(BaseModel):
    username: str
    password: str


items = {"foo": "The Foo Wrestlers"}


@router.get("/items10/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@router.post("/files5/")
async def create_file(
        file: Annotated[bytes, File()],
        fileb: Annotated[UploadFile, File()],
        token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@router.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@router.post("/login2/")
async def login(data: Annotated[FormData, Form()]):
    return data
