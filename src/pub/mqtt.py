import asyncio
from collections.abc import Iterable

from connection import Connection
from publisher import Publisher
from stream import MessageStream


class MqttPublisher(Publisher):
    def __init__(self, stream: MessageStream, connections: Iterable[Connection]):
        self._stream = stream
        self._connections = connections

    async def __aenter__(self):
        active_connections = [
            asyncio.create_task(conn.create(self._stream)) for conn in self._connections
        ]

        await asyncio.gather(*active_connections)

    async def __aexit__(self, exc_type, exc, tb):
        # TODO: Отменить задачи
        pass


# async def main():
#     print("Out publisher")
#     async with MqttPublisher(gen=['hello', 'world'], num_connections=2):
#         print("Insdie publisher")
#
# asyncio.run(main())
