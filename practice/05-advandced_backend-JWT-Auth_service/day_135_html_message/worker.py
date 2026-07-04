import os
import multiprocessing
from dotenv import load_dotenv

from celery import Celery # type: ignore
from celery.app.task import Task # type: ignore

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib

load_dotenv()

if os.name == 'nt':
    multiprocessing.set_start_method('spawn', force=True)

celery_app = Celery('send_msg_worker', broker=os.getenv('REDIS_URL'))

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

SENDER_EMAIL = os.getenv('EMAIL', 'user@example.com')
APP_PASSWORD = os.getenv('APP_PASSWORD', 'your_app_password')

def create_message(recipient: str, html_content: str, subject: str):
    msg = MIMEMultipart()

    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject

    text_content = html_content

    msg.attach(MIMEText(text_content, 'html'))

    return msg

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60) # type: ignore
def send_msg_worker(self: Task, recipient_email: str, html_string: str, subject: str):

    msg = create_message(recipient=recipient_email, html_content=html_string, subject=subject)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.set_debuglevel(1)

            server.starttls()
            server.login(user=SENDER_EMAIL, password=APP_PASSWORD)
            server.send_message(msg)
            
            print('Сообщение отправлено')
    except Exception as exc:
        print(f'Произошла ошибка: {exc}')
        raise self.retry(exc=exc) # type: ignore