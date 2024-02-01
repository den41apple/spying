from httpx import AsyncClient


async def test_not_200(async_client: AsyncClient):
    response = await async_client.get('/status')
    assert response.status_code != 200
