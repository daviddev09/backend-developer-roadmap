from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from day_141_repository_pattern.repositories.base import BaseRepository, User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=User, session=session)

    async def get_user_by_email(self, email: str):
        user = await self.session.execute(select(self.model).where(self.model.email == email)) # type: ignore
        return user.scalar_one_or_none()