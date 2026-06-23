from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import exceptions

from models import User, Post, Tag


# ============================================================
#                Check and helper functions
# ============================================================

async def check_user_exists(user_id: int, session: AsyncSession):

    stmt = select(exists().where(User.id == user_id))
    result = await session.execute(stmt)
    result = result.scalar()
    return result

async def check_tag_exists(tag_name: str, session: AsyncSession):

    result = await session.execute(select(Tag).options(selectinload(Tag.posts)).where(Tag.name == tag_name))

    tag = result.scalar_one_or_none()
    return tag
    
async def tag_parser(tag_name: str):
    result = [word for word in tag_name.strip('#').split('#') if word]
    return result

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

        error_msg = str(e.orig).lower()
        
        if 'users_email_key' in error_msg or 'email' in error_msg:
            raise exceptions.UniqueError(detail='Этот адрес электронной почты уже занят')
            
        if 'users_username_key' in error_msg or 'username' in error_msg:
            raise exceptions.UniqueError(detail='Это имя пользователя уже занято')


async def create_post(text: str, user_id:int, tag_name:str, session: AsyncSession):
    parsed_tags = await tag_parser(tag_name=tag_name)

    user = await check_user_exists(user_id=user_id, session=session)

    if user:
        
        post = Post(text=text, user_id=user_id)

        for parsed_tag in parsed_tags:
            exists_tag = await check_tag_exists(tag_name=parsed_tag, session=session)
        
            if exists_tag:
                post.tags.append(exists_tag)
            else:
                tag = Tag(name=parsed_tag)
                post.tags.append(tag)

        session.add(post)
        await session.commit()
        await session.refresh(post)

        post_tags_and_user = await get_post_by_id(post_id=post.id, session=session)
    
    
        return post_tags_and_user
    raise exceptions.EntityNotFound(detail=f'Пользователь с ID: {user_id} не найден!')

# ====================================================================
#                 Update functions
# ====================================================================
async def update_user_username(user_id: int, new_username: str, session: AsyncSession):

    result = await session.execute(select(User).options(selectinload(User.posts)).where(User.id == user_id))

    user = result.scalar_one_or_none()
    if user:
        user.username = new_username
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    raise exceptions.EntityNotFound(detail=f'Пользователь с ID: {user_id} не найден')

async def update_post(post_id: int, new_text: str|None, new_tags:str|None, session: AsyncSession):

    if new_text is None and new_tags is None:
        raise exceptions.BadRequest(detail='Вы не передали никаких данных для изменения!')
    result = await session.execute(select(Post).options(selectinload(Post.user), selectinload(Post.tags)).where(Post.id == post_id))

    post = result.scalar_one_or_none()

    if post:

        if new_text and new_tags:
            parsed_tags = await tag_parser(tag_name=new_tags)
            post.text = new_text
            post.tags.clear()
            for parsed_tag in parsed_tags:
                exists_tag = await check_tag_exists(tag_name=parsed_tag, session=session)

                if exists_tag:
                    post.tags.append(exists_tag)
                else:
                    tag = Tag(name=parsed_tag)
                    post.tags.append(tag)
                    
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

        if new_text:
            post.text = new_text
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

        if new_tags:
            parsed_tags = await tag_parser(tag_name=new_tags)
            post.tags.clear()

            for parsed_tag in parsed_tags:
                exists_tag = await check_tag_exists(tag_name=parsed_tag, session=session)

                if exists_tag:
                    post.tags.append(exists_tag)

                else:
                    tag = Tag(name=parsed_tag)
                    post.tags.append(tag)
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        
    raise exceptions.EntityNotFound(detail='Пост не найден')

# ====================================================================
#                 Delete functions
# ====================================================================

async def delete_the_user(user_id: int|None, username:str|None, session: AsyncSession):
    if user_id and username:
        raise exceptions.BadRequest(detail='Вы передали ID и имя пользователя вместе!')
    
    if not username and not user_id:
        raise exceptions.BadRequest(detail='Ошибка: Нужно передать либо имя пользлвателя либо ID')
    if user_id:
        stmt = select(User).where(User.id == user_id)
    else:
        stmt = select(User).where(User.username == username)

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise exceptions.EntityNotFound(detail='Пользователь не найден')
    
    await session.delete(user)
    await session.commit()

async def delete_post(post_id: int, session: AsyncSession):
    
    stmt = select(Post).where(Post.id == post_id)

    result = await session.execute(stmt)

    post = result.scalar_one_or_none()

    if not post:
        raise exceptions.EntityNotFound(detail='Пост не найден')
    
    await session.delete(post)
    await session.commit()
    