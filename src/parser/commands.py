import logging
from functools import wraps
from typing import Callable

from parser.data import ParsedMessage
from parser.keyword import DATA
from parser.keyword import TOPIC
from parser.registry import register


DRAW_COMMAND = 1
BRIGHTNESS_COMMAND = 2

logger = logging.getLogger(__name__)


def empty_msg_val(func: Callable):
    """Декортатор валидации пустых значений"""

    @wraps(func)
    def wrapper(msg: dict):
        if DATA not in msg or TOPIC not in msg:
            logger.error('Data or topic not found in msg')
            return None

        return func(msg)

    return wrapper


@register(command=DRAW_COMMAND)
@empty_msg_val
def parse_draw(msg: dict) -> ParsedMessage | None:
    return ParsedMessage(data=msg[DATA], topic=msg[TOPIC], command=DRAW_COMMAND)


@register(command=BRIGHTNESS_COMMAND)
@empty_msg_val
def set_brightness(msg: dict) -> ParsedMessage | None:
    if len(msg[DATA]) != 1:
        logger.error('Brightness command excpect only one element')
        return None

    return ParsedMessage(data=msg[DATA], topic=msg[TOPIC], command=BRIGHTNESS_COMMAND)


# Register commands. command.py module imported to parser.py as *
__all__ = ['parse_draw', 'set_brightness']
