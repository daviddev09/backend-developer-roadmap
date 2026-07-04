import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] | %(name)s | %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] | %(name)s | %(message)s')

file_handler = logging.FileHandler(filename='logs.log', encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def raise_exception():
    try:
        return 1 / 0
    except Exception:
        logger.error('Ошибка: деление на ноль', exc_info=True)

raise_exception()