"""
Модели запросов и ответов API
"""
from pydantic import BaseModel


class VisitedLinksRequestData(BaseModel):
    """
    Список ссылок, которые были посещены работником
    """
    links: list[str]


class VisitedLinksResponse(BaseModel):
    status: str


class VisitedDomainsResponse(BaseModel):
    domains: list[str]
    status: str
