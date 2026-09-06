"""安全相关的工具函数：密码哈希、JWT 令牌生成与验证。"""
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.schemas.auth import TokenData
from app.schemas.user import User, UserInDB

# 初始化密码哈希工具
password_hash = PasswordHash.recommended()

# 用于防止时序攻击的虚拟哈希
DUMMY_HASH = password_hash.hash("dummypassword")

# OAuth2 密码流配置（tokenUrl 是相对路径，会自动解析为 /api/v1/auth/token）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# 模拟用户数据库（真实项目应使用数据库）
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码与哈希密码是否匹配。"""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码的哈希值。"""
    return password_hash.hash(password)


def get_user(db: dict, username: str) -> UserInDB | None:
    """从数据库获取用户。"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(db: dict, username: str, password: str) -> UserInDB | bool:
    """认证用户，返回用户对象或 False。

    使用 DUMMY_HASH 防止用户名枚举时序攻击。
    """
    user = get_user(db, username)
    if not user:
        # 用户不存在时仍执行哈希验证，防止时序攻击
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建 JWT 访问令牌。"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """从 JWT 令牌中获取当前用户。"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """获取当前活跃用户（未被禁用）。"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
