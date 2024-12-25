from asyncio import Queue

from pub.stream import EndlessMessageStream


class EndlessQueueStream(EndlessMessageStream):
    def __init__(self, q: Queue):
        self._q = q

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self._q.get()
