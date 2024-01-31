"""
Операции с БД
"""
from sqlalchemy import select
from sqlalchemy.engine import Result

from db import Link
from .db import async_session


async def add_links(links: list[str]):
    """
    Добавление ссылок в БД

    Параметры:
    ----------
        links: list[str] - Список ссылок
    """
    async with async_session() as session:
        for link in links:
            link_db = Link(link=link)
            session.add(link_db)
        await session.commit()


async def get_links() -> list[Link]:
    """
    Получает список ссылок
    """
    statement = select(Link)
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        links = result.all()
    return links
