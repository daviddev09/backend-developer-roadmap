import os
import multiprocessing
from celery import Celery # type: ignore
from celery.app.task import Task # type: ignore

from dotenv import load_dotenv

load_dotenv()

if os.name == 'nt':
    multiprocessing.set_start_method('spawn', force=True)

celery_app = Celery('my_project', broker=f'{os.getenv('REDIS_URL')}')


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60) # type: ignore
def add(self: Task, a: int, b: int)->int:
    try:
        result = a + b
        return result
    except Exception as exc:
        raise self.retry(exc=exc) # type: ignore