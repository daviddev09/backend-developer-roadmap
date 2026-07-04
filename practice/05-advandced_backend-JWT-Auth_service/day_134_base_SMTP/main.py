import os
from dotenv import load_dotenv

from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib

load_dotenv()

email = os.getenv('EMAIL')
app_password = os.getenv('APP_PASSWORD')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def create_message(from_user: str, to_user: str, title: str, text: str):

    msg = MIMEMultipart()

    msg['From'] = from_user  # От кого
    msg['To'] = to_user      # Кому
    msg['Subject'] = title   # Тема письма

    text_content = text

    msg.attach(MIMEText(text_content, 'plain'))

    print(msg.as_string())
    return msg

def send_message(smtp: str, port: int, msg: Message):
    try:
        server = smtplib.SMTP(smtp, port)

        server.set_debuglevel(1)

        server.starttls()
        server.login(user=email, password=app_password) # type: ignore

        server.send_message(msg)

        print('Сообщение успешно передано серверу!')

    except Exception as e:
        print(f'Произошла ошибка при отправке. {e}')
    
    finally:
        server.quit() # type: ignore

title = '134-й день учёбы по роудмапу'
text = 'Привет! Не сдавайся и двигайся к своей цели. Ты сможешь'

message = create_message(from_user=email, to_user=email, title=title, text=text) # type: ignore
send_message(smtp=SMTP_SERVER, port=SMTP_PORT, msg=message)