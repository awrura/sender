import logging
from logging import Logger

from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import ConnectionError as RedisConnectionError


class RedisMessageQueue:
    def __init__(self, host: str, port: int, queue: str, logger: Logger | None = None):
        self._pool = AsyncConnectionPool(host=host, port=port)
        self._queue = queue
        self._logger = logger or logging.getLogger(__name__)

    async def pop(self):
        while True:
            try:
                r = AsyncRedis(connection_pool=self._pool)
                _, msg = await r.blpop(self._queue)  # pyright: ignore[reportArgumentType, reportGeneralTypeIssues]
                return msg
            except RedisConnectionError:
                self._logger.error('Unable connect to Redis. Retry soon')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._pool.aclose()
