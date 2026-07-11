import time
import asyncio
from service import UserService
from fastapi import FastAPI, Depends
from dependencies import get_service, init_models


app = FastAPI()


@app.post('/create-users-posts', status_code=200)
async def create_users_and_posts(service: UserService = Depends(get_service)):
    start_time = time.perf_counter()
    print(f'\n------------CREATING USERS AND POSTS-------------')
    
    result = await service.create_users_and_posts(username='davidev', email='david09@example.com', title='study', description='Learn advanced backend')
    print(f'\n==============SUMMARY TIME {time.perf_counter() - start_time}==========================')
    return result

@app.get('/get-users-lazy')
async def lazy_load(service: UserService = Depends(get_service)):
    start_time = time.perf_counter()
    print(f'\n-------------LAZY LOADING--------------')

    result = await service.get_users_with_posts_lazyload()

    print(f'\n==============SUMMARY TIME {time.perf_counter() - start_time}==========================')

    return result


@app.get('/get-users-eager')
async def eager_load(service: UserService = Depends(get_service)):
    start_time = time.perf_counter()
    print(f'\n-------------EAGER LOADING-------------')

    result = await service.get_users_with_posts_selectinload()
    
    print(f'\n==============SUMMARY TIME {time.perf_counter() - start_time}==========================')

    return result

if __name__ == '__main__':
    asyncio.run(init_models())