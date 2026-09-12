from typing import Annotated

from fastapi import APIRouter
from collections.abc import AsyncIterable, Iterable

from app.schemas.item import Item
from fastapi.sse import EventSourceResponse

router = APIRouter(prefix="/stream", tags=["Stream"])

items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


@router.get("/test")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


@router.get("/test2", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
