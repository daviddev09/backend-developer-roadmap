import time
import asyncio
from fastapi import FastAPI

app = FastAPI(title='Trying to block Event loop')

def generation_image(name: str)->str:
    for i in range(1, 100000):
        print(i)
    return f'{name}fxmw30f.jpg'

async def save_photo(photo: str):
    await asyncio.sleep(5)
    print(f'Profile picture {photo} has saved')

@app.get('/sync-block')
async def lock_event_loop():
    time.sleep(5)
    return

@app.get('/run-iteration')
async def run_generation_image(name: str)-> dict[str,str]:
    result: str = await asyncio.to_thread(generation_image, name)
    return {
        'status': 'success',
        'msg': 'image generated',
        'result': result
    }

@app.post('/profile-avatar')
async def save_profile_photo():
    asyncio.create_task(save_photo('avatar'))
    return{
        'status': 'success',
        'msg': 'profile picture saving on background'
    }