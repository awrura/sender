import json
import logging
from typing import TypedDict

from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis as AsyncRedis

logger = logging.getLogger(__name__)


class InputMessage(TypedDict):
    topic: str
    payload: bytes


class RedisMessageQueue:
    def __init__(self, host: str, port: int, queue: str):
        self._pool = AsyncConnectionPool(host=host, port=port)
        self._queue = queue

    # @aretry(msg='Unable connect to Redis', on_error=(RedisConnectionError,))
    async def pop(self) -> InputMessage:
        """
        Извлечь сообщение из очереди Redis

        При помощи операции blpop в Redis извлечь сообщение
        """

        r = AsyncRedis(connection_pool=self._pool)
        _, msg = await r.blpop(self._queue)  # pyright: ignore[reportArgumentType, reportGeneralTypeIssues]
        logger.info(f'Received msg from redis: {msg}')
        msg = json.loads(msg)

        logger.info(f'Parsed message: {msg}')
        return InputMessage(topic=msg['topic'], payload=msg['data'])

    async def __aenter__(self):
        logger.debug('Redis connection pool ready')
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._pool.aclose()
        logger.debug('Redis connection pool closed')
