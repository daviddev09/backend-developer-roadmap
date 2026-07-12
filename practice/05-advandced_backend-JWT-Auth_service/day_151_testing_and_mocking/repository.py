from typing import Any

from models import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_user(self, data: dict[str, Any]):
        try:
        
            user = User(**data)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        
        except SQLAlchemyError:
            await self.session.rollback()
            return None

    async def get_user_by_id(self, user_id:int):
        result = await self.session.execute(select(User).where(User.id == user_id))

        user = result.scalar_one_or_none()

        return user
    
    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))

        return result.scalar_one_or_none()

