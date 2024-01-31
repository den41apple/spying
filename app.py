"""
Запуск API
"""
from urllib.parse import urlparse

from fastapi import FastAPI
import uvicorn

from api.models import LinksRequestData, LinksResponse, DomainsResponse
from db.actions import add_links, get_links

app = FastAPI()


@app.post("/visited_links", response_model=LinksResponse)
async def visited_links(data: LinksRequestData):
    """
    Получает список ссылок, которые были посещены работником
    """
    status = "ok"
    await add_links(data.links)
    return {'status': status}


@app.get("/visited_domains", response_model=DomainsResponse)
async def visited_domains():
    """
    Получает список ссылок, которые были посещены работником
    """
    status = "ok"
    links = await get_links()
    links = [el.link for el in links]
    domains = (urlparse(el).netloc for el in links)
    domains = list(set(domains))
    return {"domains": domains,
            "status": status}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
