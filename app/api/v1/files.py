"""文件路径接口。"""
from fastapi import APIRouter

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
