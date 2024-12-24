import asyncio
from collections.abc import Iterable

from connection import StreamConnection
from stream import EndlessMessageStream


class StreamConnectionPublisher:
    """
    Отправитель сообщений из потока данных

    Представляет собой контекстный менеджер, занимающийся обработкой соединения,
    прослушивание потока данных и автоматическую отправку сообщений получателю

    >>> async with MqttPublisher(connections=[EndlessMessageStream(), EndlessMessageStream()], stream=StreamConnection()):
    >>>     your code here...
    """

    def __init__(
        self, stream: EndlessMessageStream, connections: Iterable[StreamConnection]
    ):
        self._stream = stream
        self._connections = connections
        self._active_connections = []

    async def __aenter__(self):
        self._active_connections = [
            asyncio.create_task(conn.listen(self._stream)) for conn in self._connections
        ]

        await asyncio.gather(*self._active_connections)

    async def __aexit__(self, exc_type, exc, tb):
        # TODO: Отменить задачи
        pass
