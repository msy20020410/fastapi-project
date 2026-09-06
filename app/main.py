"""FastAPI 应用入口。"""
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.schemas.exception import UnicornException
from fastapi.security import OAuth2PasswordBearer
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
)

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
