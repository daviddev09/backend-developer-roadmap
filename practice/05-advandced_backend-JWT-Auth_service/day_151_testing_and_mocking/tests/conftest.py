import asyncio
import pytest

from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from main import app
from models import Base, User
from security import get_password_hash
from dependencies import get_db_session

TEST_DATABASE_URL = 'sqlite+aiosqlite:///./app.db'

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session()-> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    
@pytest.fixture
async def client(db_session: AsyncSession)-> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session: AsyncSession):
    user = User(username='newuser', email='newuser@example.com', password_hash= await get_password_hash('secretpwd123'))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user