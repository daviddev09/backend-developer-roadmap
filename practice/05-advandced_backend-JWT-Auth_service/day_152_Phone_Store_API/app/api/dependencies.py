from app.core.uow import UnitOfWork
from app.core.security import oauth2_scheme, decode_jwt
from app.exceptions.exception import Unauthorized, AccessDenied

from app.service.user import UserService
from app.service.auth import AuthService
from app.service.cart import CartService
from app.service.phone import PhoneService
from app.service.order import OrderService

from app.models.user import User
from app.models.base import UserRole

from fastapi import Depends


async def get_uow():
    return UnitOfWork()


async def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow=uow)

async def get_phone_service(uow: UnitOfWork = Depends(get_uow)):
    return PhoneService(uow=uow)

async def get_auth_service(uow: UnitOfWork = Depends(get_uow)):
    return AuthService(uow=uow)

async def get_cart_service(uow: UnitOfWork = Depends(get_uow)):
    return CartService(uow=uow)

async def get_order_service(uow: UnitOfWork = Depends(get_uow)):
    return OrderService(uow=uow)

async def get_current_user(token: str = Depends(oauth2_scheme), uow: UnitOfWork = Depends(get_uow)):
    payload = await decode_jwt(token)

    if not payload:
        raise Unauthorized(detail='Invalid token')
    
    user_id = payload.get('sub')

    if not user_id:
        raise Unauthorized(detail='Invalid token payload')
    
    async with uow:
        user = await uow.users.get_user_by_id(int(user_id))
        if not user:
            raise Unauthorized(detail='User not found')
        return user
        
async def get_owner_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.OWNER:
        raise AccessDenied(detail='Admin access required')
    return current_user