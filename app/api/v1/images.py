"""图片接口。"""
from fastapi import APIRouter

from app.schemas.image import Image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
