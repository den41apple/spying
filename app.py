"""
Запуск API
"""
from urllib.parse import urlparse

import validators
from fastapi import FastAPI, Query
from validators import ValidationError

from api.models import VisitedLinksRequestData, VisitedLinksResponse, VisitedDomainsResponse
from db.actions import add_links, get_links

app = FastAPI()


@app.post("/visited_links", response_model=VisitedLinksResponse)
async def visited_links(data: VisitedLinksRequestData):
    """
    Отправить список ссылок, которые были посещены работником
    """
    status = "ok"
    valid_links = []
    invalid_links = []
    for link in data.links:
        if _is_valid_url(link):
            valid_links.append(link)
        else:
            invalid_links.append(link)
    if invalid_links:
        status = "Следующие ссылки имеют неверный формат и не были добавлены: "
        invalid_links = (f'"{el}"' for el in invalid_links)
        status += ",".join(invalid_links)
    if valid_links:
        await add_links(valid_links)
    return {'status': status}


def _is_valid_url(url: str) -> bool:
    """
    Проверяет валидность ссылки

    Возвращает:
    -----------
        bool
    """
    result = validators.url(url)
    if isinstance(result, ValidationError):
        return False
    return True


@app.get("/visited_domains", response_model=VisitedDomainsResponse)
async def visited_domains(_from: int = Query(None, alias="from"), to: int = None):
    """
    Получить список доменов, которые были посещены работником
    """
    status = "ok"
    domains = []
    errors = _validate_visited_domains_params(_from=_from, to=to)
    if errors:
        status = errors
    else:
        links = await get_links(_from=_from, to=to)
        links = [el.link for el in links]
        domains = (urlparse(el).netloc for el in links)
        domains = list(set(domains))
    return {"domains": domains,
            "status": status}


def _validate_visited_domains_params(_from: int | None = None,
                                     to: int | None = None) -> str:
    """
    Проверяет параметры запроса для эндпоинта "/visited_domains"

    Параметры:
    ----------
        _from: int | None - Число в timestamp
                            для фильтрации левой границы времени (Включительно)
        to: int | None - Число в timestamp
                         для фильтрации правой границы времени (Включительно)


    Возвращает:
    -----------
        str - Строка будет содержать текст если имеется ошибка
    """
    errors = []
    error_string = ""
    if _from is not None:
        if _from < 0:
            errors.append('"from" должен быть больше нуля')
    if to is not None:
        if to < 0:
            errors.append('"to" должен быть больше нуля')
    if _from is not None and to is not None:
        if _from > to:
            errors.append('"from" должен быть меньше "to"')
    if errors:
        error_string += "Ошибк"
        if len(errors) > 1:
            error_string += "и: "
        else:
            error_string += "а: "
        for i, el in enumerate(errors):
            if len(errors) > 1:
                error_string += f"{i+1})"
            error_string += el
            if len(errors) > 1:
                error_string += ". "
    return error_string.strip()
