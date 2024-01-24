"""
Create async session connect to database
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from configs.app_config import DB_USER, DB_NAME, DB_PORT, DB_HOST, DB_PASS

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DB_USER}:"
    f"{DB_PASS}@"
    f"{DB_HOST}:"
    f"{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=True,
)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session
