"""
Main configurations file for testing
"""

import asyncio
from typing import Generator, Any

import asyncpg
import pytest
from sqlalchemy import text, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette.testclient import TestClient

from configs.app_config import (
    DB_USER_TEST,
    DB_PASS_TEST,
    DB_HOST_TEST,
    DB_PORT_TEST,
    DB_NAME_TEST,
)
from src.db.session import get_db
from src.main import tracker

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://"
    f"{DB_USER_TEST}:"
    f"{DB_PASS_TEST}@"
    f"{DB_HOST_TEST}:"
    f"{DB_PORT_TEST}/"
    f"{DB_NAME_TEST}"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(
        DATABASE_URL_TEST,
    )

    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
    )

    yield async_session

    # Действия после завершения сессии, если есть
    # Закрываем соединение с базой данных
    await engine.dispose()


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            DATABASE_URL_TEST,
            echo=True,
        )

        test_async_session = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
            autoflush=True,
        )
        async with test_async_session() as session:
            yield session
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    tracker.dependency_overrides[get_db] = _get_test_db
    with TestClient(tracker) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(DATABASE_URL_TEST.split("+asyncpg")))
    yield pool
    pool.close()
