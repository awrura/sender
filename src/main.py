import asyncio
import logging.config

import yaml
from cnpool.pool import MqttConnectionPool
from pydantic_settings import BaseSettings

with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


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
    ) as pool:
        while True:
            await asyncio.sleep(5)
            await pool.send(42)
            print('HELLO!!')


if __name__ == '__main__':
    logger.info('Sender starts wake up')
    asyncio.run(main())
