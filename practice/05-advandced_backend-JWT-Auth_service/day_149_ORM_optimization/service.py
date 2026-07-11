from repository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def create_users_and_posts(self, username: str, email: str, title: str, description: str):
        users_data = [{'username': f'{username} {i}', 'email': f'{email} {i}'} for i in range(1000000)] 

        user_ids = await self.repo.create_user(data=users_data) 
        
        posts_data = [{'title': f'{title} {i}', 'description': description, 'user_id': user_id} for i, user_id in enumerate(user_ids)]
        await self.repo.create_post(posts_data)
        print(f'\n Successfully created {len(user_ids)} users and posts')
        return

    async def get_users_with_posts_lazyload(self):
        return await self.repo.get_users_posts_lazyload()
    
    async def get_users_with_posts_selectinload(self):
        return await self.repo.get_users_posts_selectinload()