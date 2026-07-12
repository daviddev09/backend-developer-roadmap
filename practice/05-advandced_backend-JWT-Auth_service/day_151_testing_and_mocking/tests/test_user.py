import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, test_user):
    response = await client.get(url=f'/users/{test_user.id}')
    
    assert response.status_code == 200

