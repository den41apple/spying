"""
Запуск API
"""
from urllib.parse import urlparse

from fastapi import FastAPI, Query

from api.models import (VisitedLinksRequestData,
                        VisitedLinksResponse,
                        VisitedDomainsResponse)
from db.actions import (add_links as _add_links,
                        get_links as _get_links)
from validator_utils import is_valid_url, validate_visited_domains_params

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
        if is_valid_url(link):
            valid_links.append(link)
        else:
            invalid_links.append(link)
    if invalid_links:
        status = "Следующие ссылки имеют неверный формат и не были добавлены: "
        invalid_links = (f'"{el}"' for el in invalid_links)
        status += ",".join(invalid_links)
    if valid_links:
        await _add_links(valid_links)
    return {'status': status}


@app.get("/visited_domains", response_model=VisitedDomainsResponse)
async def visited_domains(_from: int = Query(None, alias="from"), to: int = None):
    """
    Получить список доменов, которые были посещены работником
    """
    status = "ok"
    domains = []
    errors = validate_visited_domains_params(_from=_from, to=to)
    if errors:
        status = errors
    else:
        links = await _get_links(_from=_from, to=to)
        links = [el.link for el in links]
        domains = (urlparse(el).netloc for el in links)
        domains = list(set(domains))
    return {"domains": domains,
            "status": status}
