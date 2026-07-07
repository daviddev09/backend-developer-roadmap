from core.database import AsyncSessionLocal
from repositories.user import UserRepository


class UnitOfWork:
    def __init__(self) -> None:
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb): # type: ignore

        if exc_type is not None:
            await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()