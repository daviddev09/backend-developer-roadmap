from app.core.uow import UnitOfWork
from app.schemes.order import PlaceOrderRead
from app.exceptions.exception import EntityNotFound, BadRequest, Unauthorized, CodeTimeOut, InsufficientStock

from enum import Enum
from typing import Any

class OrderStatus(Enum):
    PAID = 'paid'
    SHIPPING = 'shipping'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class OrderService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def _create_order_data(self, user_id: int, cart_total_cost: int, address: str)-> dict[str, Any]:
        return {
                'user_id': user_id,
                'total_cost': cart_total_cost,
                'address': address,
                'order_items': []
            }
    
    def _create_order_item_data(self, order_id: int, phone_id: int, phone_quantity: int)->dict[str, int]:
        return {
            'order_id': order_id,
            'phone_id': phone_id,
            'phone_quantity': phone_quantity
        }
    
    def _create_four_digit_code(self):
        import random
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        code = ''
        for i in range(4):
            num = random.choice(nums)
            code += str(num)
        return code

    async def get_my_orders(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_user_and_orders(user_id)
            if not user:
                raise Unauthorized(detail='Пользователь не найден. Возможно неавторизован')
            return user
    
    async def place_order(self, address: str, user_id: int, cart_id: int):
        async with self.uow:
            user = await self.uow.users.get_user_and_orders(user_id)
            cart = await self.uow.carts.get_cart(cart_id)

            if not user:
                raise EntityNotFound(detail='User not found')
            if not cart:
                raise EntityNotFound(detail='Cart Not found')
            
            if not cart.cart_items:
                raise BadRequest(detail='Чтобы оформить заказ требуется чтобы в корзине было минимум один товар!')
            
            order_data = self._create_order_data(user_id=user.id, cart_total_cost=cart.total_cost, address=address)

            order = await self.uow.orders.create_order(order_data)
            
            for cart_item in cart.cart_items:

                order_item_data = self._create_order_item_data(order_id=order.id, phone_id=cart_item.phone_id, phone_quantity=cart_item.phone_quantity)
                order_item = await self.uow.orders.create_order_item(order_item_data)
                order.order_items.append(order_item)

                await self.uow.carts.delete_from_cart(cart_id=cart.id, phone_id=cart_item.phone.id)
                cart.total_cost -= cart_item.phone_quantity * cart_item.phone.price
            
            user.orders.append(order)  # type: ignore
            await self.uow.commit()
            return await self.uow.orders.get_order(order_id=order.id)
        
    async def pay_for_the_order(self, user_id: int, order_id: int)-> dict[str, Any]:
        async with self.uow:
            user = await self.uow.users.get_user_and_orders(user_id)
        
            if not user:
                raise Unauthorized(detail='Пользователь не найден либо сделал выход')
            if not user.orders: # type: ignore
                raise EntityNotFound(detail='У вас нет никаких заказов')
            
            orders = await self.uow.orders.get_orders(user_id)

            exists_order = None
            for order in orders:
                if order.id == order_id:
                    exists_order = order

            if not exists_order:
                raise EntityNotFound(detail='Такого заказа нет')
            if exists_order.status == OrderStatus.PAID:
                raise BadRequest(detail='Заказ уже оплачен')
            if exists_order.status == OrderStatus.SHIPPING:
                raise BadRequest(detail='Заказ уже в пути')
            if exists_order.status == OrderStatus.DELIVERED:
                raise BadRequest(detail='Заказ уже доставлен')
            if exists_order.status == OrderStatus.CANCELLED:
                raise BadRequest(detail='Заказ отменён')
            
            order_scheme = PlaceOrderRead.model_validate(exists_order)
            msg = f'{user.username} вы оплачиваете заказ по ID: {exists_order.id} стоимостью {exists_order.total_cost}, чтобы подтвердить оплату, введите 4 значный код в эндпоинт [Confirm payment] который мы отправили на вашу почту: {user.email}. Важно: код дейтсвителен только 60 секунд, если вы не получили код попробуйте оформить оплату заново' # type: ignore
            code = self._create_four_digit_code()

            await self.uow.caches.add_pay_confirmate_code_to_cache(user.id, exists_order.id, code) # type: ignore
            self.uow.register_task(
                task_name='app.workers.worker.send_confirmation_code_msg_worker',
                recipient_email=user.email,
                subject='Подтверждение оплаты',
                name=user.username,
                order_cost=exists_order.total_cost,
                code=code
                )
            
            await self.uow.commit()
            return {
                'message': msg,
                'Your order': order_scheme
            }

    async def confirmation_payment(self, user_id: int, confirm_code: str):
        async with self.uow:
            code_cache = await self.uow.caches.get_pay_confirmate_code_cache(user_id)

            if not code_cache:
                raise CodeTimeOut(detail='Срок действия кода истёк')
            
            if code_cache.code != confirm_code:
                await self.uow.caches.delete_pay_confirmate_code_from_cache(user_id)
                raise BadRequest(detail='Неправильный код подтверждения оплаты. Код будет аннулирован')
            
            await self.uow.caches.delete_pay_confirmate_code_from_cache(user_id)

            user = await self.uow.users.get_user_by_id(user_id)
            order = await self.uow.orders.get_order(code_cache.order_id)
            if not user:
                raise EntityNotFound(detail='Пользователь не найден')
            if not order:
                raise EntityNotFound(detail='Заказ не найден')
            
            for order_item in order.order_items:
                phone_id = order_item.phone_id
                quantity = order_item.phone_quantity
                phone = await self.uow.phones.get_phone_by_id(phone_id)
                if not phone:
                    order.status = f'{OrderStatus.CANCELLED}'
                    raise InsufficientStock(detail=f'Телефона: {order_item.phone.name} не осталось, оформляйте заказ заново, ваши деньги не будут списаны')
                if phone.stock_quantity - quantity < 0:
                    order.status = f'{OrderStatus.CANCELLED}'
                    raise InsufficientStock(detail=f'Нету телефонов {phone.name}в количестве: {quantity}, возможно пока вы оформляли заказ кто-то уже купил')

                phone.stock_quantity -= quantity
            order.status = f'{OrderStatus.PAID}'
            self.uow.register_task(
                task_name='app.workers.worker.shipment_order_worker',
                recipient_email=user.email,
                recipient_name=user.username,
                order_id=order.id
            )
            await self.uow.commit()

            return {
                'msg': f'Ваш заказ успешно оплачен и очень скоро будет отправлен в путь! При отправке вашего заказа, мы отправим сообщение на вашу почту: {user.email}'
            }