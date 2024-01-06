"""
Create async session connect to database
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session
