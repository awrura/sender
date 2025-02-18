import logging

import parser.commands as comma  # import just for run decorators
from parser.data import ParsedMessage
from parser.keyword import COMMAND
from parser.registry import get_parser

logger = logging.getLogger(__name__)
# Fucking pre-commit
_ = comma


def parse(msg: dict) -> ParsedMessage | None:
    """
    Распарсить сообщение

    Для каждой команды используется свой специфичный парсер.
    Логика этого инкапсулирована.

    :return: Структурированное сообщение или None
    если парсинг не удался
    """

    if COMMAND not in msg:
        logger.error('Command not found in message')
        return None

    parse_func = get_parser(msg[COMMAND])
    if not parse_func:
        logger.error(f'Parser for command {msg[COMMAND]} not found')
        return None

    return parse_func(msg)
