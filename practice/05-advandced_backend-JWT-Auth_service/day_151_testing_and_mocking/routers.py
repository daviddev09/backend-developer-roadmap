from service import UserService
from security import oauth2scheme
from dependencies import get_service
from schemas import UserCreate, UserRead

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

app_router = APIRouter()

@app_router.post('/users', response_model=UserRead)
async def create_user(data: UserCreate, service: UserService = Depends(get_service)):
    user = await service.create_user(data=data)

    if user:
        return user
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@app_router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(get_service)):
    jwt_token = await service.login(username=form_data.username, password=form_data.password)

    if jwt_token == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    
    if jwt_token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return jwt_token

@app_router.get('/users/me', response_model=UserRead)
async def get_cuurent_user(token: str = Depends(oauth2scheme), service: UserService = Depends(get_service)):
    return await service.get_me(token)

@app_router.get('/users/{user_id}', response_model=UserRead)
async def get_user(user_id: int, service: UserService = Depends(get_service)):
    return await service.get_user_by_id(user_id=user_id)


