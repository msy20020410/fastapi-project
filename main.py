"""项目入口，保持 `fastapi dev` 与 `uvicorn main:app` 兼容。"""
from app.main import app

__all__ = ["app"]
