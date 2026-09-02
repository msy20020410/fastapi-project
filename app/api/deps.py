"""全局认证依赖:校验请求头 `X-Token` / `X-Key`。

企业级要点:
- 校验逻辑独立成依赖,避免定义在入口模块造成的反向导入循环;
- 使用 `secrets.compare_digest` 做常量时间比较,防时序攻击;
- 认证失败返回 401(Unprocessable 之外的标准语义),并附 `WWW-Authenticate` 头以便客户端重放认证;
- 凭证从配置注入,不硬编码。
"""
from secrets import compare_digest
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.config import settings

unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid X-Token / X-Key credentials",
    headers={"WWW-Authenticate": "Token"},
)


def verify_token(
    x_token: Annotated[str, Header()],
) -> None:
    from secrets import compare_digest

    if not x_token or not compare_digest(x_token, settings.api_token):
        raise unauthorized


def verify_key(
    x_key: Annotated[str, Header()],
) -> None:
    if not x_key or not compare_digest(x_key, settings.api_key):
        raise unauthorized


# 组合依赖:一处声明,各处复用
verify_auth = Annotated[None, Depends(verify_token), Depends(verify_key)]

__all__ = ["verify_auth", "verify_token", "verify_key"]
