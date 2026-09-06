"""FastAPI 应用入口。"""
import time

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.schemas.exception import UnicornException

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)


@app.on_event("startup")
def on_startup():
    """应用启动时初始化数据库。"""
    create_db_and_tables()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(
        request: Request,
        exc: UnicornException
):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something."
        },
    )


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Hello World"}
