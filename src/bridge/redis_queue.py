import json
import logging
from typing import TypedDict

from aioredis import ConnectionPool as AsyncConnectionPool
from aioredis import Redis as AsyncRedis
from aioredis.exceptions import RedisError
from parser.parser import parse
from utils.retry import aretry

logger = logging.getLogger(__name__)


class InputMessage(TypedDict):
    topic: str
    payload: bytes


class RedisMessageQueue:
    def __init__(self, host: str, port: int, queue: str):
        self._pool = AsyncConnectionPool(host=host, port=port)
        self._queue = queue

    @aretry(msg='Unable connect to Redis', on_error=(RedisError,))
    async def pop(self) -> InputMessage:
        """
        Извлечь сообщение из очереди Redis

        При помощи операции blpop в Redis извлечь сообщение
        """

        r = AsyncRedis(connection_pool=self._pool)

        while True:
            _, msg = await r.blpop(self._queue)
            logger.info('Received msg from redis')
            msg = json.loads(msg)
            pmsg = parse(msg)
            if pmsg:
                break

        return InputMessage(
            topic=pmsg.topic,
            payload=bytes([pmsg.command, *pmsg.data]),
        )

    async def __aenter__(self):
        logger.debug('Redis connection pool ready')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._pool.disconnect()
        logger.debug('Redis connection pool closed')
