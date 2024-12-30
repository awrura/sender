import asyncio

from cnpool.pool import MqttConnectionPool
from pydantic_settings import BaseSettings


class MqttConfig(BaseSettings):
    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_LOGIN: str
    MQTT_PASS: str
    MQTT_TOPIC: str

    class Config:
        env_file = '.env'


async def main():
    conf = MqttConfig()  # pyright: ignore[reportCallIssue]

    async with MqttConnectionPool(
        hostname=conf.MQTT_HOST,
        port=conf.MQTT_PORT,
        login=conf.MQTT_LOGIN,
        password=conf.MQTT_PASS,
        target_topic=conf.MQTT_TOPIC,
    ) as connection:
        while True:
            await asyncio.sleep(5)
            await connection.send(42)
            print('HELLO!!')


if __name__ == '__main__':
    print('Hello world')
    asyncio.run(main())
