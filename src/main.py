import asyncio

from cnpool.pool import ConnectionPool


async def main():
    conf = {
        'MQTT_HOST': 'localhost',
        'MQTT_PORT': 1883,
        'MQTT_LOGIN': 'user1',
        'MQTT_PASS': 'main',
    }
    async with ConnectionPool(
        hostname=conf['MQTT_HOST'],
        port=conf['MQTT_PORT'],
        login=conf['MQTT_LOGIN'],
        password=conf['MQTT_PASS'],
        target_topic='hello',
    ) as connection:
        while True:
            await asyncio.sleep(5)
            await connection.send(42)
            print('HELLO!!')


if __name__ == '__main__':
    print('Hello world')
    asyncio.run(main())
