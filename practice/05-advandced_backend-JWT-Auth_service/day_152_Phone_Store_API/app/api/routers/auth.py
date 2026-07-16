from app.models.user import User
from app.schemes.user import UserCreate, UserRead

from app.service.auth import AuthService
from app.core.security import set_refresh_cookie
from app.api.dependencies import get_auth_service, get_current_user

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Cookie, Response


app_router = APIRouter(prefix='/auth', tags=['Authorization'])


@app_router.post('/register', response_model=UserRead)
async def register(
    data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    """
    Регистрирует пользователя (Создаёт данные в БД).
    username и email должны быть уникальными и регистрироваться можно только по gmail почте. 
    Чтобы получить роль Owner пользователя в системе, нужно регистрироваться под email: david@example.com
    После регистрации требуется вход по замку в Swagger (если используется Swagger UI).
    """
    return await service.register(data)

@app_router.post('/login')
async def login(
    response: Response,
    data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    """
    Функция логина. при входе создаёт токены и возвращает их клиенту
    """
    access_token, refresh_token = await service.login(username=data.username, password=data.password)

    await set_refresh_cookie(response=response, refresh_token=refresh_token) # type: ignore

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }

@app_router.post('/refresh')
async def refresh(
    response: Response,
    refresh_token: str|None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service)
):
    """
    Функция обновления токенов. Берёт refresh token из куки и обновляет оба токена
    """
    access_token, new_refresh_token = await service.refresh_token(refresh_token)

    await set_refresh_cookie(response=response, refresh_token=new_refresh_token)

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
    
@app_router.delete('/logout')
async def logout(
    refresh_token: str|None = Cookie(default=None),
    _: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    """
    Функция выхода из системы.
    Использовать его могут только авторизованные пользователи
    """
    return await service.logout(refresh_token)
