import pytest
from main import app
from httpx import AsyncClient, ASGITransport


class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


async def create_user_json(name: str, email: str) -> dict[str, str]:
    return {
        'name': name,
        'email': email
    }


@pytest.fixture(scope='function')
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


async def test_create_user(client: AsyncClient):
    true_user: User = User(name='daviddev', email='daviddev@example.com')
    false_user_name: User = User(name='d', email='daviddev@example.com')
    false_user_email: User = User(name='daviddev', email='daviddevexample.com')

    true_result = await client.post(url='/users/create/user', json=await create_user_json(name=true_user.name, email=true_user.email))
    false_name_result = await client.post(url='/users/create/user', json=await create_user_json(name=false_user_name.name, email=false_user_name.email))
    false_email_result = await client.post(url='/users/create/user', json=await create_user_json(name=false_user_email.name, email=false_user_email.email))

    assert true_result.status_code == 200
    assert true_result.json()['name'] == 'daviddev'

    assert false_name_result.status_code == 422

    assert false_email_result.status_code == 422