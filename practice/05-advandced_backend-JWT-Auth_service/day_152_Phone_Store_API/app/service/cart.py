from app.core.uow import UnitOfWork
from app.schemes.cart import CartItemRead
from app.exceptions.exception import EntityNotFound, InsufficientStock, BadRequest
from typing import Any


class CartService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _calculate_stock_quantity(self, cart_dto: CartItemRead):
        for cart_item in cart_dto.cart_items:
            cart_item.phone.stock_quantity -= cart_item.phone_quantity
        return cart_dto

    async def get_cart(self, cart_id: int):
        async with self.uow:
            cart = await self.uow.carts.get_cart(cart_id)
            if not cart:
                raise EntityNotFound(detail='Cart not found, the ID might be incorrect')
            return self._calculate_stock_quantity(CartItemRead.model_validate(cart))

    async def add_to_cart(self, cart_id: int, phone_id: int, quantity: int):
        if quantity < 1:
            raise BadRequest(detail='Количество не может быть меньше одного')
        async with self.uow:
            
            phone = await self.uow.phones.get_phone_by_id(phone_id)
            cart = await self.uow.carts.get_cart(cart_id)

            if not phone:
                raise EntityNotFound(detail='Phone not found')
            
            if not cart:
                raise EntityNotFound(detail='Cart not found')
            
            if phone.stock_quantity < quantity:
                raise InsufficientStock(detail='Not enough in stock')
        
            existing_item = None
            if cart.cart_items:
                for cart_item in cart.cart_items:
                    if cart_item.phone.id == phone_id:
                        existing_item = cart_item
                        break

            total_cost = phone.price * quantity

            if existing_item:
                if existing_item.phone_quantity + quantity > phone.stock_quantity:
                    raise InsufficientStock(detail='Not enough in stock')        
                existing_item.phone_quantity += quantity
                cart.total_cost += total_cost
                    
            else:
                data: dict[str, Any] = {'phone_quantity': quantity, 'phone': phone}
                cart.total_cost += total_cost
                cart = await self.uow.carts.add_to_cart(cart_id, data=data)

            await self.uow.commit()
            
            return self._calculate_stock_quantity(CartItemRead.model_validate(cart))

    async def remove_from_cart(self, cart_id: int, phone_id: int, quantity: int):
        if quantity < 1:
            raise BadRequest(detail='Количество не может быть меньше одного')
        async with self.uow:
            phone = await self.uow.phones.get_phone_by_id(phone_id)
            cart = await self.uow.carts.get_cart(cart_id)
            

            if not phone:
                raise EntityNotFound(detail='Phone not found')
            
            if cart:
                if not cart.cart_items:
                    raise BadRequest(detail='Удалять нечего')
                
                index=0
                existing_item = None
                for i, cart_item in enumerate(cart.cart_items):
                    if cart_item.phone_id == phone_id:
                        index = i
                        existing_item = cart_item
                        break

                if not existing_item:
                    raise EntityNotFound(detail='Такого телефон в корзине нет')
                

                if existing_item.phone_quantity - quantity <= 0:
                    deleted_item = cart.cart_items.pop(index)
                    cart.total_cost -= deleted_item.phone_quantity * deleted_item.phone.price
                    
                else:
                    existing_item.phone_quantity -= quantity
                    cart.total_cost -= existing_item.phone.price * quantity
                    
                await self.uow.commit()
                return self._calculate_stock_quantity(CartItemRead.model_validate(cart))
            
    async def delete_from_cart(self, cart_id: int, phone_id: int):
        async with self.uow:

            phone = await self.uow.phones.get_phone_by_id(phone_id)
            cart = await self.uow.carts.get_cart(cart_id)

            if not phone:
                raise EntityNotFound(detail='Phone not found')
            
            if not cart:
                raise EntityNotFound(detail='Cart not found')
            
            if not cart.cart_items:
                raise BadRequest(detail='Удалять нечего')
            
            exists_item = None
            for cart_item in cart.cart_items:
                if cart_item.phone_id == phone_id:
                    exists_item = cart_item
                    break
                
            if not exists_item:
                raise EntityNotFound(detail='Такого товара в корзине нет')
            
            await self.uow.carts.delete_from_cart(cart_id, phone_id)
            cart.total_cost -= exists_item.phone_quantity * exists_item.phone.price
            await self.uow.commit()
            await self.uow.session.refresh(cart)
            return self._calculate_stock_quantity(CartItemRead.model_validate(cart))