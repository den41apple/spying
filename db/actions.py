"""
Операции с БД
"""
from datetime import datetime

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


async def get_links(_from: int | None = None,
                    to: int | None = None) -> list[Link]:
    """
    Получает список ссылок

    Параметры:
    ----------
        _from: int | None - Число в timestamp
                            для фильтрации левой границы времени (Включительно)
        to: int | None - Число в timestamp
                         для фильтрации правой границы времени (Включительно)

    Возвращает:
    ----------
        list[Link] - Список с объектами ссылок
    """
    statement = select(Link)
    if _from:
        _from = datetime.fromtimestamp(_from)
        statement = statement.where(Link.created_at >= _from)
    if to:
        to = datetime.fromtimestamp(to)
        statement = statement.where(Link.created_at <= to)
    statement = statement.distinct()
    async with async_session() as session:
        result: Result = await session.scalars(statement)
        links = result.all()
    return links
