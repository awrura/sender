import logging
from typing import Callable

__COMMAND_ROUTES = {}

logger = logging.getLogger(__name__)


def register(command: int):
    """Декоратор регистрации комманд"""

    def wrapper(func: Callable):
        __COMMAND_ROUTES[command] = func
        logger.info(f'Register command {command} to <func {func.__name__}>')
        return func

    return wrapper


def get_parser(command: int) -> Callable | None:
    """
    Получить ссылку на функцию,
    которая парсит сообщение для данной команды
    """

    return __COMMAND_ROUTES.get(command, None)
