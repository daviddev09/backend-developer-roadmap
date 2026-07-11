from typing import Any

from models import User, Post

from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

class UserPostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_users(self, data: list[dict[str, Any]]):
        result = await self.session.execute(insert(User).returning(User.id), data)
        return result.scalars().all()
    
    async def create_posts(self, data: list[dict[str, Any]]):
        await self.session.execute(insert(Post), data)
        return
    
    async def get_user_by_id(self, user_id:int):
        result = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.posts)))

        user = result.scalar_one_or_none()

        return user
    
    async def get_post_by_id(self, post_id: int):
        result = await self.session.execute(select(Post).where(Post.id == post_id))

        post = result.scalar_one_or_none()

        return post
    
    async def get_paginated_posts(self, last_post_id: int):
        stmt = select(Post)
        
        if last_post_id > 0:
            stmt = stmt.where(Post.id > last_post_id)

        stmt = stmt.order_by(Post.id.asc()).limit(20)

        result = await self.session.scalars(stmt)
        return result.all()
    

