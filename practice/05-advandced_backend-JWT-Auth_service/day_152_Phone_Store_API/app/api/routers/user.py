from app.service.user import UserService
from app.api.dependencies import get_user_service, get_current_user, get_owner_user
from app.schemes.user import UserRead, UserUpdate, UserCartReadForOwner
from app.models.user import User

from fastapi import APIRouter, Depends


app_router = APIRouter(prefix='/users', tags=['Users'])

@app_router.get('/me', response_model=UserRead)
async def get_me(
    user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """
    Получает профиль текущего пользователя.
    Использовать может только авторизованный пользователь
    """
    return await service.get_user(user_id=user.id)


@app_router.put('/profile/{user_id}', response_model=UserRead)
async def update(
    user_update: UserUpdate,
    user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """
    Изменяет профиль текущего пользователя.
    Использовать может только авторизованный пользователь
    """
    return await service.change_profile(user_id=user.id, data=user_update)

@app_router.get('/{user_id}', response_model=UserCartReadForOwner)
async def get_user(
    user_id: int,
    _: User = Depends(get_owner_user),
    service: UserService = Depends(get_user_service)
):
    """
    Получает данные пользователя по id.
    Может получать данные любых авторизованных пользователей.
    Может использовать только пользователь с ролью Owner
    """
    return await service.get_user(user_id=user_id)

@app_router.delete('/delete-user/{user_id}', status_code=200)
async def delete(
    user_id: int,
    _: User = Depends(get_owner_user),
    service: UserService = Depends(get_user_service)
):
    """
    Удаляет пользователя по id.
    Использовать может только пользователь с ролью Owner.
    Пользователь с ролью Owner не может удалить другого пользователя с ролью Owner
    """
    return await service.delete(user_id)