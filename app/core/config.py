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

    # 数据库配置
    database_url: str = "sqlite:///./database.db"
    echo_sql: bool = True


settings = Settings()
