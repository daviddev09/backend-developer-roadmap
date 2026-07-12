import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    json = {'username': 'daviddev', 'email': 'daviddev09@example.com', 'password':'secretpwd123'}

    response = await client.post(url='/users', json=json,)

    assert response.status_code == 200
    data = response.json()

    assert data['username'] == 'daviddev'
    assert data['email'] == 'daviddev09@example.com'
    assert 'password' not in data

@pytest.mark.asyncio
async def test_duplicate_email(client: AsyncClient, test_user):
    response = await client.post(
        '/users',
        json={
            'username': 'unknownuser',
            'email': 'newuser@example.com',
            'password': 'secretpwd123'
        },
    )

    assert response.status_code == 409