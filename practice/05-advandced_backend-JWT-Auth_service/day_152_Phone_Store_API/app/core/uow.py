from app.core.database import AsyncSessionLocal, redis_client
from app.repository.user import UserRepository
from app.repository.cart import CartRepository
from app.repository.phone import PhoneRepository
from app.repository.order import OrderRepository
from app.repository.cache import CacheRepository
from app.repository.session import SessionRepository

from celery.canvas import Signature # type: ignore
from typing import Any

class UnitOfWork:
    def __init__(self) -> None:
        self.session_factory = AsyncSessionLocal
        self.redis_client = redis_client
        self.tasks_to_run: list[dict[str, Any]] = []

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.carts = CartRepository(self.session)
        self.phones = PhoneRepository(self.session)
        self.orders = OrderRepository(self.session)
        self.refresh_sessions = SessionRepository(self.session)
        self.caches = CacheRepository(redis_client=self.redis_client)

    def register_task(self, task_name: str, **kwargs: Any):
        task: dict[str, Any] = {'task_name': task_name, 'kwargs': kwargs}
        self.tasks_to_run.append(task)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb): # type: ignore

        if exc_type is not None:
            await self.session.rollback()

        self.tasks_to_run.clear()
        await self.session.close()


    async def commit(self):
        await self.session.commit()
        from app.workers.worker import celery_app
        for task in self.tasks_to_run:
            celery_app.send_task(task['task_name'], kwargs=task['kwargs']) # type: ignore
        
        self.tasks_to_run.clear()

    async def rollback(self):
        await self.session.rollback()
        self.tasks_to_run.clear()