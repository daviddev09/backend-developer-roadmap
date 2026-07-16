from app.models.user import User
from app.service.order import OrderService
from app.schemes.order import PlaceOrderRead, UserOrdersRead
from app.api.dependencies import get_order_service, get_current_user

from fastapi import APIRouter, Body, Depends


app_router = APIRouter(prefix='/orders', tags=['Orders'])


@app_router.post('/place', response_model=PlaceOrderRead)
async def place_order(
    address: str = Body(examples=['Tokyo, Japan']),
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    """
    Эндпоинт оформляющий заказ. 
    Принимает адрес для доставки. 
    При оформлении создаёт заказ и добавляет а него все товары из корзины, и очищает корзину. 
    """
    return await service.place_order(address=address, user_id=user.id, cart_id=user.cart.id)
    
@app_router.post('/pay/{order_id}')
async def pay_for_order(
    order_id: int,
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    """
    Эндпоинт оформления оплаты заказа. 
    Принимает ID заказа и отправляет в почту 4-значный код с подтверждением оплаты, 
    код аннулируется через 60 секунд после создания или после одной неудачной попытки, а деньги не списываются. 
    Переводит товар с статуса: pending, в paid.
    Чтобы подтвердить оплату нужно вводить код в эндпоинт: POST [confirm_pament]
    """
    return await service.pay_for_the_order(user_id=user.id, order_id=order_id)

@app_router.post('/post/pay/confirmate')
async def confirm_payment(
    code: int,
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    """
    Эндпоинт подтверждения заказа. 
    Принимает 4-значный код подтверждения отправленный на почту.
    После успешной оплаты отправляет товар в очередь для доставки, 
    Меняет статус заказа с: paid, на: shipping. 
    И в скором времени когда товар уже отправляют в путь, отпавляет письмо 
    на почту, с датой доставки"""
    return await service.confirmation_payment(user_id=user.id, confirm_code=str(code))

@app_router.get('/my/orders', response_model=UserOrdersRead)
async def get_my_orders(
    user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service)
):
    """
    Эндпоинт получения списков всех своих заказов, даже отменённых
    """
    return await service.get_my_orders(user_id=user.id)
