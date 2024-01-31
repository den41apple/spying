"""
Запуск API
"""
from fastapi import FastAPI
import uvicorn

from api.models import LinksRequestData, LinksResponse

app = FastAPI()


@app.post("/visited_links", response_model=LinksResponse)
async def visited_links(data: LinksRequestData):
    """
    Получает список ссылок, которые были посещены работником
    """
    pass
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
