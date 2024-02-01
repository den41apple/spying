import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import app
from db.db import async_session, async_engine, metadata


@pytest.fixture(autouse=True, scope="function")
async def prepare_database():
    """
    Подготавливает БД
    """
    async with async_engine.begin() as connection:
        await connection.run_sync(metadata.create_all)
    yield
    async with async_engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def session() -> AsyncSession:
    """
    Сессия БД
    """
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client():
    """
    Http клиент
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client
