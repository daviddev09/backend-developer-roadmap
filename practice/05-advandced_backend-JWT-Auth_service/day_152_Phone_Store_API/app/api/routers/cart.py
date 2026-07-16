from app.models.user import User
from app.service.cart import CartService
from app.schemes.cart import CartItemRead
from app.api.dependencies import get_cart_service, get_current_user

from fastapi import APIRouter, Depends, Query


app_router = APIRouter(prefix='/cart', tags=['Cart'])

@app_router.get('/get-my-cart', response_model=CartItemRead)
async def get_cart(
    user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    """
    Получает корзину пользователя.
    Использовать могут только авторизованные пользователи
    """
    return await service.get_cart(cart_id = user.cart.id) # type: ignore

@app_router.post('/add-to-cart/{phone_id}', response_model=CartItemRead)
async def add_to_cart(
    phone_id: int,
    phone_quantity: int = Query(examples=['Например 1 000 000']),
    user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    """
    Добавляет в корзину пользователя телефон.
    Нужно передать id телефона и количество.
    Использовать могут только авторизованные пользователи
    """
    return await service.add_to_cart(cart_id=user.cart.id, phone_id=phone_id, quantity=phone_quantity)

@app_router.post('/remove-from-cart/{phone_id}', response_model=CartItemRead)
async def remove_from_cart(
    phone_id: int,
    phone_quantity: int = Query(examples=['Например 1']),
    user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    """
    Удаляет из корзины пользователя телефон по количеству.
    Нужно передать id телефона и количество.
    Использовать могут только авторизованные пользователи
    """
    return await service.remove_from_cart(cart_id=user.cart.id, phone_id=phone_id, quantity=phone_quantity)

@app_router.post('/delete-from-cart/{phone_id}', response_model=CartItemRead)
async def delete_from_cart(
    phone_id: int,
    user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service)
):
    """
    Удаляет из корзины пользователя телефон во всех количествах.
    Нужно передать id телефона.
    Использовать могут только авторизованные пользователи"""
    return await service.delete_from_cart(cart_id=user.cart.id, phone_id=phone_id)