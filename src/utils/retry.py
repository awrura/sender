import asyncio
import logging
from functools import wraps
from typing import Type

logger = logging.getLogger(__name__)


def aretry(
    msg: str,
    on_error: tuple[Type[Exception]],
    start_delay_sec: int = 2,
    max_delay_sec: int = 128,
):
    """
    Декоратор повторного вызова в случае возникновения ошибок

    Пытается повторно вызвать декорируемую функцию в случае возникновения ошибок
    После каждого неудачного вызова ожидает некоторе время, после чего пытается снова

    :param msg: Сообщение которое вывести в лог при возникновении ошибки
    :param on_error: Типы ошибок, при которых необходимо повторно вызывать декорируемую функцию
    :param start_delay_sec: Начальное время ожидания. После каждой неудачи оно увеличивается в 2 раза
    :param max_delay_sec: Максимальное время ожидания
    """

    def safe_call(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = start_delay_sec
            while True:
                try:
                    await func(*args, **kwargs)
                except on_error:
                    logger.error(f'{msg}. Retry after {current_delay} sec')
                    await asyncio.sleep(current_delay)
                    current_delay = min(current_delay * 2, max_delay_sec)

        return wrapper

    return safe_call
