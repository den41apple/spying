"""
Модели запросов и ответов API
"""
from pydantic import BaseModel


class LinksRequestData(BaseModel):
    """
    Список ссылок, которые были посещены работником
    """
    links: list[str]


class LinksResponse(BaseModel):
    status: str
