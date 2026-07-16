from app.models.user import User
from app.models.base import UserRole
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem

from typing import Any

from sqlalchemy.orm import selectinload
from sqlalchemy import select, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    
    async def create_user(self, data: dict[str, Any]):
        user = User(**data)

        self.session.add(user)
        await self.session.flush()
        return user
    

    async def get_user_by_id(self, user_id: int):
        result = await self.session.execute(select(User).options(selectinload(User.orders), selectinload(User.cart).selectinload(Cart.cart_items).selectinload(CartItem.phone)).where(User.id == user_id)) # type: ignore
        
        return result.scalar_one_or_none()

    async def get_user_and_orders(self, user_id: int):
        result = await self.session.execute(
            select(User).options(selectinload(User.orders).selectinload(Order.order_items).selectinload(OrderItem.phone), selectinload(User.cart)).where(User.id == user_id) # type: ignore
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).options(selectinload(User.orders), selectinload(User.cart).selectinload(Cart.cart_items)).where(User.username == username)) # type: ignore
        
        return result.scalar_one_or_none()
    
    
    async def check_exists_user_by_email(self, email: str):
        result = await self.session.execute(select(exists(User).where(User.email == email)))
        return result.scalar()
    
    async def chechk_exists_user_username(self, username: str):
        result = await self.session.execute(select(exists(User).where(User.username == username)))
        return result.scalar()

    async def check_exists_user_by_id(self, user_id: int):
        return await self.session.scalar(select(exists(User).where(User.id == user_id)))
    
    async def check_role_user(self, user_id: int):
        return await self.session.scalar(select(exists(User).where(User.id == user_id, User.role == UserRole.OWNER)))


    async def change_profile(self, user_id: int, new_data: dict[str, Any]):
        user = await self.get_user_by_id(user_id=user_id)

        if user:
            for key, value in new_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await self.session.flush()
            return user
    

    async def delete_user(self, user_id: int):
        await self.session.execute(delete(User).where(User.id == user_id))
        return