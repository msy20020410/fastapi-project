"""数据库连接和会话管理。"""
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=settings.echo_sql,
    connect_args={"check_same_thread": False}  # SQLite 需要这个配置
)


def create_db_and_tables():
    """创建所有数据库表。"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """获取数据库会话的依赖注入函数。"""
    with Session(engine) as session:
        yield session
