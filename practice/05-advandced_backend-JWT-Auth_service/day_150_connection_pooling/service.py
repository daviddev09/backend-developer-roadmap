from typing import Any
from repository import UserPostRepository


class UserPostService:
    def __init__(self, repo: UserPostRepository) -> None:
        self.repo = repo

    async def create_users_and_posts(self):
        data = [{'username':'davidev', 'email': f'daviddev0{i}@example.com'} for i in range(1,1001)]
        user_ids = await self.repo.create_users(data=data) # type: ignore
        
        post_data = [{'title': 'STUDY', 'description': f'Day_{i}', 'user_id': id} for i, id in enumerate(user_ids)] # type: ignore
        await self.repo.create_posts(data=post_data) # type: ignore
        await self.repo.session.commit()
        return {'status': 'success'}
    
    async def get_user_by_id(self, user_id: int):
        return await self.repo.get_user_by_id(user_id=user_id)
    
    async def get_post_by_id(self, post_id: int):
        return await self.repo.get_post_by_id(post_id=post_id)
    
    async def get_paginated_posts(self, last_id: int)-> Any:
        posts = await self.repo.get_paginated_posts(last_post_id=last_id)
        last_post_id = posts[-1].id
        
        return {
            'last_id': last_post_id,
            'posts': posts
        }
        

