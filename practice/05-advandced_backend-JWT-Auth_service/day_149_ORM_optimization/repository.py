from typing import Any
from models import User, Post
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, data: list[dict[str, Any]]):
        stmt = insert(User).returning(User.id)
        result = await self.session.execute(stmt, data)
        await self.session.commit()
        return result.scalars().all()
    
    
    async def create_post(self, data: list[dict[str, Any]]):
        await self.session.execute(insert(Post), data)
        await self.session.commit()
        
        


    async def get_users_posts_lazyload(self):
        users = await self.session.scalars(select(User))

        for user in users:
            posts = await self.session.scalars(select(Post).where(Post.user_id == user.id))

            print(f'Посты пользователя {user.username}: {posts}')


    async def get_users_posts_selectinload(self):
        users = await self.session.scalars(select(User).options(selectinload(User.posts)))
        
        for user in users:
            print(f'Посты пользователя {user.username}: {user.posts}')