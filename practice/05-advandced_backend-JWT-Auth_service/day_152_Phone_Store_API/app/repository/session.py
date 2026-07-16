from app.models.session import RefreshSession

from typing import Any
from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_session(self, data: dict[str, Any]):

        refresh_session = RefreshSession(**data)
        self.session.add(refresh_session)
        await self.session.flush()
        return refresh_session
    

    async def check_exists_session_by_user_id(self, user_id: int):
        return await self.session.scalar(select(exists(RefreshSession).where(RefreshSession.user_id == user_id)))

    async def check_exists_session(self, token: str):
        return await self.session.scalar(select(exists(RefreshSession).where(RefreshSession.refresh_token == token)))
    
    async def get_refresh_token(self, token: str):
        result = await self.session.execute(select(RefreshSession).where(RefreshSession.refresh_token == token))
        return result.scalar_one_or_none()

    
    async def delete_session_by_token(self, token: str):
        return await self.session.execute(delete(RefreshSession).where(RefreshSession.refresh_token == token))

    async def delete_session_by_user_id(self, user_id: int):
        return await self.session.execute(delete(RefreshSession).where(RefreshSession.user_id == user_id))