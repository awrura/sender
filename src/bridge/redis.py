from dataclasses import dataclass

from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import ConnectionError
from redis.exceptions import TimeoutError


@dataclass
class RedisConnectConfig:
    HOST: str
    PORT: int
    QUEUE: str


class Retriever:
    def __init__(self, redis: AsyncRedis, target_queue: str):
        self._redis = redis
        self._queue = target_queue

    async def pop(self):
        _, msg = await self._redis.blpop(self._queue)  # pyright: ignore[reportArgumentType, reportGeneralTypeIssues]
        return msg


class RedisMessageQueue:
    def __init__(self, host: str, port: int, queue: str):
        self._config = RedisConnectConfig(host, port, queue)
        self._redis: AsyncRedis

    async def __aenter__(self):
        conf = self._config
        self._redis = AsyncRedis(
            host=conf.HOST,
            port=conf.PORT,
            retry_on_error=[ConnectionError, TimeoutError],
        )
        return Retriever(self._redis, conf.QUEUE)

    async def __aexit__(self, exc_type, exc, tb):
        await self._redis.close()
