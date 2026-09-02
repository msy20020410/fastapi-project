from typing import Annotated

from fastapi import FastAPI, Header,APIRouter
from pydantic import BaseModel



class CommonHeaders(BaseModel):
    id: str
    name: str
    age: str | None = None

router = APIRouter(prefix="/headers", tags=["Headers"])


@router.get("/headers/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers