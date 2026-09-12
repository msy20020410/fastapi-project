"""v1 版本路由汇总。"""
from fastapi import APIRouter

from app.api.v1 import files, images, items, ml_models, users, weights, cookies, headers, login, tools, heroes, stream
from app.schemas import exception

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(items.router)
api_router.include_router(users.router)
api_router.include_router(images.router)
api_router.include_router(files.router)
api_router.include_router(ml_models.router)
api_router.include_router(weights.router)
api_router.include_router(cookies.router)
api_router.include_router(headers.router)
api_router.include_router(login.router)
api_router.include_router(tools.router)
api_router.include_router(heroes.router)
api_router.include_router(stream.router)

