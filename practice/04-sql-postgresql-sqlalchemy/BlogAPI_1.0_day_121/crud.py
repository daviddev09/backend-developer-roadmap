from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import exceptions

from models import User, Post, Tag
# ============================================================
#                 Read functions
# ============================================================



async def get_user_by_id(user_id: int, session: AsyncSession):

    result = await session.execute(select(User).options(selectinload(User.posts)).where(User.id == user_id))

    user = result.scalar_one_or_none()
    if user:
        return user
    raise exceptions.EntityNotFound(detail=f'Пользователь с ID: {user_id} не найден')


async def get_user_by_username(username: str, session: AsyncSession):

    result = await session.execute(select(User).options(selectinload(User.posts)).where(User.username == username))

    user = result.scalar_one_or_none()
    if user:
        return user
    raise exceptions.EntityNotFound(detail=f'Пользователь с именем пользователя {username} не найден')

async def get_post_by_id(post_id:int, session: AsyncSession):

    result = await session.execute(select(Post).options(selectinload(Post.user), selectinload(Post.tags)).where(Post.id == post_id))

    post = result.scalar_one_or_none()
    if post:
        return post
    raise exceptions.EntityNotFound(detail=f'Пост с ID: {post_id} не найден')


# ====================================================================
#                 Create functions
# ====================================================================

async def create_user(username:str, email:str, session: AsyncSession):
    try:
        user = User(username=username, email=email)

        session.add(user)
        await session.flush()
        await session.commit()
        await session.refresh(user)
        return user
    except IntegrityError as e:
        await session.rollback()

        if 'UNIQUE' in str(e.orig).upper():
            raise exceptions.UniqueError(detail='Этот адрес электронной почты уже занят')


async def create_post(text: str, user_id:int, session: AsyncSession):
    post = Post(text=text, user_id=user_id)

    session.add(post)
    await session.commit()
    await session.refresh(post)
    
    return post

async def add_tag(tag_name: str, post_id: int, session: AsyncSession):
    post = await get_post_by_id(post_id=post_id, session=session)
    tag = Tag(name=tag_name)
    
    if post:
        post.tags.append(tag)

    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return tag