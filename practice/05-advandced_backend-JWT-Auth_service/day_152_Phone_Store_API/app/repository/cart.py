from app.models.cart import Cart, CartItem

from typing import Any
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession

class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_cart(self, user_id: int):
        cart = Cart(user_id=user_id)
        self.session.add(cart)
        await self.session.flush()
        return cart
    
    async def add_to_cart(self, cart_id: int, data: dict[str, Any]):

        cart = await self.get_cart(cart_id)
        if cart:
            
            cart_item = CartItem(**data)
            cart.cart_items.append(cart_item)
            await self.session.flush()
            return cart
        

    async def check_exists_cart(self, cart_id: int):
        cart = await self.session.execute(select(exists(Cart).where(Cart.id == cart_id)))
        return cart.scalar()
    
    async def get_cart(self, cart_id: int):
        cart = await self.session.execute(select(Cart).options(selectinload(Cart.cart_items).selectinload(CartItem.phone)).where(Cart.id == cart_id))
        return cart.scalar_one_or_none()

    
    async def delete_from_cart(self, cart_id:int, phone_id: int):
        await self.session.execute(delete(CartItem).where(CartItem.cart_id == cart_id, CartItem.phone_id == phone_id))
        return