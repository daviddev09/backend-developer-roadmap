import time
from fastapi import FastAPI, BackgroundTasks

app = FastAPI(title='Learning BackgroundTasks')

def send_welcome_email(email: str):
    print(f'\nОтправка письма на почту {email}')
    time.sleep(3)
    print('Письмо успешно доставлено')

@app.post('/register')
async def register(email: str, backgroundtasks: BackgroundTasks):
    backgroundtasks.add_task(send_welcome_email, email)
    return {
        'status': 'successfully registered',
        'msg': 'message is send to your email'
    }