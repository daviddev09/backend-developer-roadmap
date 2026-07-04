from fastapi import FastAPI
from worker import send_msg_worker

app = FastAPI()

async def create_html_template(name: str):
    html_template = f"""
    <html>
    <body>
    <h1> {name} Вы пытаетесь войти в аккаунт </h1>
    <p> Чтобы войти в аккаунт нажмите на кнопку [Подтвердить аккаунт] если это не вы то можете пропускать мимо </p>
    <a href="https://example.com"> Подтвердить аккаунт </a>
    </body>
    </html>"""
    return html_template


@app.post('/register')
async def register_the_user(name: str, email: str):
    html = await create_html_template(name=name)

    send_msg_worker.delay(recipient_email=email, html_string=html, subject='Login Confirmation') # type: ignore

    return {'message': f'Письмо подтверждения отправлено на почту: {email} зайдите и подтвердите что это действительно вы. Если письмо не пришло, нажмите [Отправить снова]'}