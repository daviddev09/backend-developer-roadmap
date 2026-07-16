from app.models.order import Order, OrderItem

from typing import Any
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, data: dict[str, Any])-> Order:
        order = Order(**data)
        self.session.add(order)
        await self.session.flush()
        return order
    
    async def create_order_item(self, data: dict[str, int]):
        order_item = OrderItem(** data)

        self.session.add(order_item)
        await self.session.flush()
        return order_item
    

    async def check_exists_order(self, order_id: int):
        order = await self.session.execute(select(exists(Order).where(Order.id == order_id)))
        return order.scalar()
    
    async def get_order(self, order_id: int):
        order = await self.session.execute(select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.phone)).where(Order.id == order_id))
        return order.scalar_one_or_none()

    async def get_orders(self, user_id: int):
        orders = await self.session.scalars(select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.phone)).where(Order.user_id == user_id))
        return orders.all()


    async def delete_order(self, order_id: int):
        await self.session.execute(delete(Order).where(Order.id == order_id))
        return