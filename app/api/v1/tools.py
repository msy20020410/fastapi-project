from typing import Annotated

from fastapi import APIRouter, Depends, Cookie
from pydantic import BaseModel

from app.schemas.exception import UnicornException

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("/globalHeadertest/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
        q: Annotated[str, Depends(query_extractor)],
        last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@router.get("/default_query/")
async def read_query(
        query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}


@router.get("/getCommonsDep/")
async def read_items(commons: CommonsDep):
    return commons


@router.get("/getCommon/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
