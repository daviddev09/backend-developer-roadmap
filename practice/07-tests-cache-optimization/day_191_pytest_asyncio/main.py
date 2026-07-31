from fastapi import FastAPI, HTTPException, status, Body
app = FastAPI()

users_db: list[dict[str, str]] = []


@app.post('/users/create/user', status_code=200)
async def create_user(name: str = Body(), email: str = Body()) -> dict[str, str]:

    if len(name) < 2 or '@' not in email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    user = {
        'name': name,
        'email': email
    }
    users_db.append(user)

    return user
