import os
import time
import multiprocessing
from dotenv import load_dotenv

from celery import Celery # type: ignore
from celery.app.task import Task # type: ignore

load_dotenv()

if __name__ == 'nt':
    multiprocessing.set_start_method('spawn', force=True)

backend: str|None = os.getenv('REDIS_URL')

celery_app = Celery(
    'my_tasks',
    broker=os.getenv('REDIS_URL'),
    backend=f'{backend[0:-1]}1' # type: ignore
)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60) # type: ignore
def heavy_computation(self: Task, a: int, b: int):
    try:
        time.sleep(10)
        return a + b
    except Exception as e:
        raise self.retry(exc=exc) # type: ignore