from typing import Annotated

from fastapi import Cookie, FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/cookies", tags=["Cookies"])


class Cookies(BaseModel):
    id: str
    name: str | None = None
    age: int | None = None


@router.get("/cookies/01")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
