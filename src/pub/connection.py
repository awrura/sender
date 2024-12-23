from typing import Protocol

import aiomqtt
from stream import MessageStream


class Connection(Protocol):
    async def create(self, stream: MessageStream):
        pass


class ConnectionMqtt(Connection):
    async def create(self, stream: MessageStream):
        async with aiomqtt.Client(
            hostname='localhost', port=1883, username='user1', password='main'
        ) as client:
            async for m in stream:
                await client.publish('test', payload=f'{m}')
