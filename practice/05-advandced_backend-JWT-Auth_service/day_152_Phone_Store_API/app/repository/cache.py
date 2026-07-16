from app.schemes.cache import PayCacheRead

import json
from redis.asyncio import Redis # type: ignore


class CacheRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client


    async def add_pay_confirmate_code_to_cache(self, user_id: int, order_id: int, payment_code: str):
        cache_key = f'user:{user_id}:pay'
        data: dict[str, int|str] = {'order_id': order_id,'code': payment_code}
        await self.redis.setex(name=cache_key, time=60, value=json.dumps(data)) # type: ignore


    async def get_pay_confirmate_code_cache(self, user_id: int):
        cache_key = f'user:{user_id}:pay'
        raw_data = await self.redis.get(cache_key) # type: ignore
        if not raw_data:
            return None

        data = json.loads(raw_data) # type: ignore
        return PayCacheRead(**data)
        

    async def delete_pay_confirmate_code_from_cache(self, user_id: int):
        cache_key = f'user:{user_id}:pay'
        return await self.redis.delete(cache_key)