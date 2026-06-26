import asyncio
from fastapi import FastAPI, Depends, Response, Cookie
from schemes import UserCreate, UserRead, LoginRequest
from dependencies import get_service, AuthService, init_models, REFRESH_TOKEN_DAYS

app = FastAPI()

@app.post('/register', tags=['Auth'])
async def create_account(data: UserCreate, response: Response, service: AuthService=Depends(get_service))-> dict[str,UserRead|str]:
    user, access_token, refresh_token = await service.register_a_user(username=data.username, email=data.email, password=data.password)

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=REFRESH_TOKEN_DAYS * 24 * 60 * 60
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'Created_user': user
    }

@app.post('/login', tags=['Auth'])
async def login(request: LoginRequest, response: Response, service: AuthService=Depends(get_service)):
    access_token, refresh_token = await service.login_function(email=request.email, password=request.password)

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=REFRESH_TOKEN_DAYS * 24 * 60 * 60
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }

@app.post('/refresh', tags=['Auth'])
async def refresh_token(refresh_token: str|None = Cookie(None), service: AuthService=Depends(get_service)):
    return await service.refresh_token(token=refresh_token)

@app.post('/logout', tags=['Auth'])
async def logout(response: Response, refresh_token: str|None = Cookie(None), service: AuthService=Depends(get_service)):
    response.delete_cookie('refresh_token')
    return await service.logout_user(refresh_token)

if __name__ == '__main__':
    
    asyncio.run(init_models())

