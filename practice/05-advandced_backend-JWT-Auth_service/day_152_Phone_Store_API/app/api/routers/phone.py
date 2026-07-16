from app.models.user import User
from app.service.phone import PhoneService
from app.api.dependencies import get_phone_service, get_owner_user
from app.schemes.phone import PhoneCreate, FullPhoneRead, PhoneUpdate


from fastapi import APIRouter, Depends, Query


app_router = APIRouter(prefix='/phones', tags=['Phones'])


@app_router.post('/add', response_model=FullPhoneRead)
async def add_phone_to_db(
    data: PhoneCreate,
    service: PhoneService = Depends(get_phone_service),
    _: User = Depends(get_owner_user)
):
    """
    Создаёт новую запись телефона в БД.
    Использовать может только пользователь с ролью Owner
    """
    return await service.create_phone(data)


@app_router.get('/search', response_model=list[FullPhoneRead])
async def search_by_name(
    phone_name: str,
    service: PhoneService = Depends(get_phone_service)
):
    """
    Поисковик.
    Возвращает список телефонов
    """
    return await service.search_phones(phone_name)

@app_router.get('/{phone_id}', response_model=FullPhoneRead)
async def search_phone_by_id(
    phone_id: int,
    service: PhoneService = Depends(get_phone_service)
):
    """
    Ищет телефон по id
    """
    return await service.get_phone_by_id(phone_id)

@app_router.get('/', response_model=list[FullPhoneRead])
async def get_paginated_phones(
    last_phone_id: int = Query(default=0),
    service: PhoneService = Depends(get_phone_service)
):
    """
    Категория телефонов. Пагинация для прокручивания товаров.
    """
    return await service.get_phones(last_phone_id)

@app_router.put('/change/{phone_id}', response_model=FullPhoneRead)
async def change_phone_data(
    phone_id: int,
    phone_update: PhoneUpdate,
    _: User = Depends(get_owner_user),
    service: PhoneService = Depends(get_phone_service)
):
    """
    Меняет данные телефона по id.
    Использовать может только пользователь с ролью Owner
    """
    return await service.update_phone(phone_id, phone_update)

@app_router.delete('/delete/{phone_id}')
async def delete_phone(
    phone_id: int,
    _: User = Depends(get_owner_user),
    service: PhoneService = Depends(get_phone_service)
):
    """
    Удаляет телефон по id.
    Использовать может только пользователь с ролью Owner
    """
    return await service.delete_phone(phone_id)