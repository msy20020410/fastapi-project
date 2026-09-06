"""应用配置(使用 pydantic-settings 从环境变量注入)。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置,枚举字段可通过环境变量覆盖,例如 `API_TOKEN`。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "FastAPI Project"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    # JWT 安全配置
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
