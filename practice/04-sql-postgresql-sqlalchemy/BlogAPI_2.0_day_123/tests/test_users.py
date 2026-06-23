import pytest
from httpx import AsyncClient

async def create_user(client: AsyncClient):
    response = await client.post(url='/users', json={'username':'david','email':'david@example.com'})

    user = response.json()

    return user

async def get_id(client: AsyncClient):
    user = await create_user(client=client)

    return user['id']

async def get_username(client: AsyncClient):
    user = await create_user(client=client)

    return user['username']


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(url='/users', json={'username':'david','email':'david@example.com'})
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient):
    user_id = await get_id(client=client)
    response = await client.get(url=f'/users/{user_id}')

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_user_by_username(client: AsyncClient):
    username = await get_username(client=client)
    response = await client.get(url='/users', params={'username':username})

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_user_username(client: AsyncClient):
    user_id = await get_id(client=client)
    response = await client.put(url=f'/users/{user_id}', json='daviddev09')

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user_with_id(client: AsyncClient):
    user_id = await get_id(client=client)
    response = await client.delete(url='/users', params={'user_id': user_id})

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user_with_username(client: AsyncClient):
    username = await get_username(client=client)
    response = await client.delete(url='/users', params={'username': username})

    assert response.status_code == 200