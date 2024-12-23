from typing import Protocol


class Publisher(Protocol):
    async def __aenter__(self):
        raise NotImplementedError('It is a abstract realisation')

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError('It is a abstract realisation')
