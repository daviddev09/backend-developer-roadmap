import pytest
from httpx import AsyncClient


async def created_user(client: AsyncClient):
    response = await client.post(url='/users', json={'username':'david','email':'david@example.com'})
    return response.json()

async def created_post(client: AsyncClient):
    user = await created_user(client=client)
    user_id = user['id']
    response = await client.post(url=f'/posts/{user_id}', json={'text':'daviddevs test'}, params={'tag_name': '#SQL #Programming'})
    
    return response.json()

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient) -> None:
    user = await created_user(client=client)
    user_id = user['id']
    response = await client.post(
        f"/posts/{user_id}",
        json={
            "text": "daviddevs test"
        },
        params={'tag_name':'#SQL #Programming'}
    )

    if response.status_code == 422:
        print(response.json())
    assert response.status_code == 200

    data = response.json()

    assert data['text'] == 'daviddevs test'


@pytest.mark.asyncio
async def test_get_post(client: AsyncClient):
    post = await created_post(client=client) # type: ignore
    response = await client.get(f'/posts/1')

    assert response.status_code == 200

    data = response.json()

    assert data['text'] == 'daviddevs test'

@pytest.mark.asyncio
async def test_update_post_text(client: AsyncClient):
    post = await created_post(client=client) # type: ignore

    response = await client.put(url=('/posts/1'),json={'new_text':'daviddevs_test'})

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_post_tags(client: AsyncClient):
    post = await created_post(client=client) # type: ignore

    response = await client.put(url='/posts/1', json={'new_tags': '#tests #tags'})

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient):
    post = await created_post(client=client) # type: ignore

    response = await client.delete(url='/posts/1')

    assert response.status_code == 200