import asyncio
import os
from random import randint

from conn.mqtt import MqttConnection
from conn.mqtt import MqttConnectionConfg
from pub.publisher import StreamConnectionPublisher
from stream.fake import EndlessQueueStream


async def adder(q: asyncio.Queue):
    while True:
        await asyncio.sleep(1)
        a = randint(1, 100)
        await q.put(a)
        print(f'ADD {a} to queue')


async def main():
    print(f'PID: {os.getpid()}')
    q = asyncio.Queue()
    asyncio.create_task(adder(q))

    stream = EndlessQueueStream(q=q)
    conf = MqttConnectionConfg(
        MQTT_HOST='localhost',
        MQTT_PORT=1883,
        MQTT_LOGIN='user1',
        MQTT_PASS='main',
        MQTT_TOPIC='nigga',
    )
    connestions = [MqttConnection(conf=conf) for _ in range(2)]
    async with StreamConnectionPublisher(stream=stream, connections=connestions):
        print('INSIDE')


if __name__ == '__main__':
    print('Hello world')
    asyncio.run(main())
