import pytest
from httpx import AsyncClient


async def created_user(client: AsyncClient):
    response = await client.post(url='/users', json={'username':'david','email':'david@example.com'})
    return response.json()

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient) -> None:
    user =await created_user(client=client)
    user_id = user['id']
    response = await client.post(
        f"/posts/{user_id}",
        json={
            "text": "daviddevs test",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data['text'] == 'daviddevs test'

@pytest.mark.asyncio
async def test_get_post(client: AsyncClient):

    response = await client.get(f"/posts/{1}")

    assert response.status_code == 200

    data = response.json()

    assert data['text'] == 'daviddevs test'
