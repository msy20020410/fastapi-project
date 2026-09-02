from typing import Annotated

from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/login", tags=["Login"])


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
