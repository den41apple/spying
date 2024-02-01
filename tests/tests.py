import pytest
from httpx import AsyncClient


async def test_status_ok(async_client: AsyncClient):
    response = await async_client.post("/visited_links",
                                       json={"links": ["http://google.com"]})
    assert response.status_code == 200
    response = await async_client.get("/visited_domains")
    assert response.status_code == 200


async def test_satus_not_ok(async_client: AsyncClient):
    # Запросы с неправильными методами
    response = await async_client.get("/visited_links")
    assert response.status_code != 200
    response = await async_client.post("/visited_domains")
    assert response.status_code != 200


async def test_send_valid_links(async_client: AsyncClient):
    response = await async_client.post("/visited_links",
                                       json={"links": ["http://google.com"]})
    assert response.json()["status"] == "ok"


async def test_send_invalid_links(async_client: AsyncClient):
    response = await async_client.post("/visited_links",
                                       json={"links": ["http:google.com"]})
    assert response.json()["status"] != "ok"


async def test_send_empty_links(async_client: AsyncClient):
    response = await async_client.post("/visited_links")
    assert response.status_code == 200
    assert response.json()["status"] != "ok"


async def test_valid_domains(async_client: AsyncClient):
    links = ("https://www.google.com/search?q=query1",
             "https://www.facebook.com/profile.php?id=12345",
             "https://www.twitter.com/user1/status/987654321",
             "https://www.twitter.com/user1/status/9344654321",
             "https://www.linkedin.com/in/user-profile",
             "https://www.reddit.com/r/subreddit/comments/abc123/title3",
             "https://www.reddit.com/r/subreddit/comments/abc123/title")
    domains = {"www.google.com", "www.facebook.com", "www.twitter.com",
               "www.linkedin.com", "www.reddit.com"}
    response = await async_client.post("/visited_links",
                                       json={"links": links})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    response = await async_client.get("/visited_domains")
    response_json = response.json()
    assert response.status_code == 200
    assert "domains" in response_json
    response_domains: list = response_json["domains"]
    assert set(response_domains) == domains


@pytest.mark.parametrize("_from, to", [
    (100, 0),
    (-1, -1),
    (None, -1),
    (-1, None),
])
async def test_invalid_visited_domains_params(async_client: AsyncClient, _from: int, to: int):
    params = {}
    if _from is not None:
        params["from"] = _from
    if to is not None:
        params["to"] = to
    response = await async_client.get("/visited_domains", params=params)
    assert response.status_code == 200
    assert response.json()["status"] != "ok"
