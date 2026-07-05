import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = jsonlogger.JsonFormatter('%(timestamp)s %(levelname)s %(message)s') # type: ignore

console_handler = logging.StreamHandler()

file_handler = RotatingFileHandler(filename='app.log', maxBytes=1 * 1024 * 1024, backupCount=3)


console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

for n in range(100001):
    logger.info(f'Message--{n}--')