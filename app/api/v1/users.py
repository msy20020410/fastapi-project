"""Users 相关接口。"""
from typing import Any

from fastapi import APIRouter

from app.schemas.user import UserIn, BaseUser

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


@router.get("/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
