"""Items 相关接口。

`/items/03`、`/items/06`、`/items/12` 等编号路径与通配路径
`/items/{item_id}` 形状相同，FastAPI 按注册顺序取第一个匹配，
因此固定路径必须全部注册在通配路径之前。
"""
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Cookie, Path, Query, Header
from fastapi.encoders import jsonable_encoder

from app.schemas.item import FilterParams, Item, Item2, Item3, Item4, Item8
from app.schemas.user import User

router = APIRouter(prefix="/items", tags=["Items"])
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.put("/items99/{item_id}", response_model=Item8)
async def update_item(item_id: str, item: Item8):
    update_item_encoded = jsonable_encoder(item)
    print(f"type: {type(update_item_encoded)}, {update_item_encoded}")
    items[item_id] = update_item_encoded
    return update_item_encoded


@router.post("/items/myItem1")
async def create_item(item: Item8) -> Item8:
    return item


@router.get("/items/myItem3", status_code=201)
async def create_item(name: str):
    return {"name": name}


@router.get("/items/myItem2")
async def read_items() -> list[Item8]:
    return [
        Item8(name="Portal Gun", price=42.0),
        Item8(name="Plumbus", price=32.0),
    ]


@router.get("/test/19/")
async def read_items(authorization: Annotated[str | None, Header()] = None):
    return {"authorization": authorization}


@router.get("/12")
async def read_cookie(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


@router.put("/11/{item_id}")
async def update_item_datetime(
        item_id: UUID,
        start_datetime: Annotated[datetime, Body()],
        end_datetime: Annotated[datetime, Body()],
        process_after: Annotated[timedelta, Body()],
        repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process

    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


@router.put("/10/{item_id}")
async def update_item_nested_model(item_id: int, item: Item4):
    results = {"item_id": item_id, "item": item}
    return results


@router.put("/09/{item_id}")
async def update_item_set_tags(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results


@router.put("/08/{item_id}")
async def update_item_embedded_body(
        item_id: int, item: Annotated[Item2, Body(embed=True)]
):
    results = {"item_id": item_id, "item": item}
    return results


@router.put("/07/{item_id}")
async def update_item_multi_body(
        item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@router.get("/06")
async def read_items_filter_params(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@router.get("/05/{item_id}")
async def read_item_path_and_query(
        item_id: Annotated[int, Path(title="The ID of the item to get")],
        q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@router.get("/04")
async def read_items_query_alias(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/03")
async def read_items_list_query(q: Annotated[list[int] | None, Query()] = None):
    return {"q": q}


@router.get("/02/")
async def read_items_required_query(q: Annotated[str | None, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/")
async def read_items(q: Annotated[str | None, Query(max_length=10, min_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.post("/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.get("/{item_id}")
async def read_item_required_params(
        item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@router.put("/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
