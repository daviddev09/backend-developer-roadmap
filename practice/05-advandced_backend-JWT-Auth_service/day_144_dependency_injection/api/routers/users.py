from fastapi import APIRouter, Depends, HTTPException, status

from services.user import UserService
from api.dependencies import get_user_service
from schemas.user import UserCreate, UserRead
from exceptions.user import EmailExistsException


router = APIRouter(prefix='/users', tags=['Users'], )


@router.post('/', response_model=UserRead)
async def register(data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return await service.register_the_user(data=data)
    except EmailExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Этот email занят')
    