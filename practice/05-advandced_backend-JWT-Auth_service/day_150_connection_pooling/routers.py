from dependencies import get_service
from service import UserPostService

from fastapi import APIRouter, Depends, Query

app_router = APIRouter()

@app_router.post('/create-all', status_code=200)
async def create_users_and_posts(service: UserPostService = Depends(get_service)):
    return await service.create_users_and_posts()

@app_router.get('/user/{user_id}')
async def get_user(user_id: int, service: UserPostService = Depends(get_service)):
    return await service.get_user_by_id(user_id=user_id)

@app_router.get('/post/{id}')
async def get_post(post_id: int, service: UserPostService = Depends(get_service)):
    return await service.get_post_by_id(post_id=post_id)

@app_router.get('/posts')
async def get_paginated_posts(last_id: int = Query(0, description='ID последнего поста с предыдущей страницы'), service: UserPostService = Depends(get_service)):
    return await service.get_paginated_posts(last_id = last_id)