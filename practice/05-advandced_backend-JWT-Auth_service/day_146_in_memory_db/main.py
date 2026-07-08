import json
import asyncio
import redis.asyncio as redis # type: ignore



async def main():
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
    try:

        user_profile = {'id': 1, 'username': 'Daviddev09', 'achievements': {'graduation': 'secondary school', 'calisthenics':{'first element': 'Handstand', 'last element': 'One arm Handstand 3 sec'}}} # type: ignore

        profile_json = json.dumps(user_profile)
        cache_key = f'user:{user_profile["id"]}:profile'

        await redis_client.setex(name=cache_key, time=10, value=profile_json) # type: ignore

        cached_data = await redis_client.get(cache_key) # type: ignore

        if cached_data:
            print(cached_data) # type: ignore

        await asyncio.sleep(11)
        deleted_data = await redis_client.get(cache_key) # type: ignore

        if deleted_data is None:
            print('Данные автоматически удалились из памяти')

    except Exception as e:
        print(f' Произошла ошибка: {e}')

    finally:
        await redis_client.close()

if __name__ == '__main__':
    asyncio.run(main())
    