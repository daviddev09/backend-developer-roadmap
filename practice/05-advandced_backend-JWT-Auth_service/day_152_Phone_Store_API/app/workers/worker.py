from app.core.config import settings

import os
import multiprocessing

from celery import Celery # type: ignore
from celery import Task # type: ignore
from redis import Redis # type: ignore

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


if os.name == 'nt':
    multiprocessing.set_start_method('spawn', force=True)

celery_app = Celery(
    'my-tasks',
    broker=settings.REDIS_URL,
    )
redis = Redis(host='localhost', port=6379, db=2, decode_responses=True)

def create_payment_html_template(name: str, order_cost: int, cnfirmation_code: str):
    html_template = f"""
    <html>
    <body>
    <h1> {name} Вы пытаетесь оплатить заказ стоимостью ${order_cost} </h1>
    <p> Чтобы подтвердить оплату введите этот код [{cnfirmation_code}] код действителен только 60 секунд. </p>
    <a phone_store.example.com ссылка на наш сайт </a>
    </body>
    </html>"""
    return html_template

def create_register_html_template(name: str, email: str, confirmation_code: str):
    html_template = f"""
    <html>
    <body>
    <h1> {name} Вы пытаетесь зарегистрироваться на наш сайт: "daviddev_phones.com" используя эту почту:{email} </h1>
    <p> Чтобы подтвердить регистрацию введите этот код [{confirmation_code}] код действителен только 60 секунд. </p>
    <a phone_store.example.com ссылка на наш сайт </a>
    </body>
    </html>"""
    return html_template

def create_shipping_order_html_template(name: str, order_id: int, order_cost: int, orderer_address: str):
    html_template = f"""
    <html>
    <body>
    <h1> {name} благодарим за покупку из нашего магазина. Ваш заказ уже в пути.</h1>
    <p> Заказ по ID: {order_id} стоимостью: ${order_cost} будет доставлен в адрес: {orderer_address} в течении: 3-4 дня </p>
    </body>
    </html>"""
    return html_template

def create_message(recipient: str, html_content: str, subject: str):
    msg = MIMEMultipart()

    msg['From'] = settings.EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject

    text_content = html_content

    msg.attach(MIMEText(text_content, 'html'))

    return msg

@celery_app.task(name='app.workers.worker.send_confirmation_code_msg_worker',bind=True, max_retries=2, default_retry_delay=10) # type: ignore
def send_confirmation_code_msg_worker(self: Task, recipient_email: str, subject: str, name: str, code: str, order_cost: int|None = None, email: str|None = None):
    if order_cost and subject=='Подтверждение оплаты':
        html_content = create_payment_html_template(name, order_cost, code)

    if email and subject=='Подтверждение регистрции':
        html_content = create_register_html_template(name, email, code)
    
    msg = create_message(recipient_email, html_content, subject)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.set_debuglevel(1)

            server.starttls()
            server.login(settings.EMAIL, settings.APP_PASSWORD)
            server.send_message(msg)
            print('Сообщение отправлено')
    except Exception as exc:
        print(f'Fail {exc}')
        raise self.retry(exc=exc) # type: ignore
    
@celery_app.task(bind=True, max_retries=100, default_retry_delay=60) # type: ignore
def send_message(self: Task, recipient_email: str, html_content: str, subject: str, order_id: int|None = None):
    if redis.get(f'order_sent:{order_id}'):
        return
    message = create_message(recipient_email, html_content, subject)
    try:

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.set_debuglevel(1)

            server.starttls()
            server.login(settings.EMAIL, settings.APP_PASSWORD)
            server.send_message(message)
            redis.setex(name=f'order_sent:{order_id}', time=6000, value='true') # type: ignore
            
            print('Сообщение отправлено')
            
    except Exception as exc:
        print(f'Fail {exc}')
        raise self.retry(exc=exc) # type: ignore

@celery_app.task(name='app.workers.worker.shipment_order_worker', bind=True, max_retries=100, default_retry_delay=60)    # type: ignore
def shipment_order_worker(
        self: Task,
        recipient_email: str,
        recipient_name: str,
        order_id: int,
):
    async def process():
        from app.core.uow import UnitOfWork
        uow = UnitOfWork()
        async with uow:
            order = await uow.orders.get_order(order_id)
            if not order:
                raise ValueError('Order not found')
            
            order.status = 'shipping'
            await uow.commit()
            return order
    try:
        import asyncio
        order = asyncio.run(process())
        html_content = create_shipping_order_html_template(recipient_name, order.id, order.total_cost, order.address)
        send_message.delay(recipient_email, html_content, 'Уведомление об отправке заказа', order_id) # type: ignore
    except Exception as exc:
        print(f'Fail {exc}')
        self.retry(exc=exc) # type: ignore