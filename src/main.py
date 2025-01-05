import asyncio
import logging.config

import yaml
from pydantic_settings import BaseSettings

with open('logging.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

from bridge.redis_queue import RedisMessageQueue  # noqa: E402
from cnpool.pool import MqttConnectionPool  # noqa: E402


class Config(BaseSettings):
    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_LOGIN: str
    MQTT_PASS: str
    MQTT_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_QUEUE: str

    class Config:
        env_file = '.env'


async def main():
    conf = Config()  # pyright: ignore[reportCallIssue]

    mqtt_pool = MqttConnectionPool(
        hostname=conf.MQTT_HOST,
        port=conf.MQTT_PORT,
        login=conf.MQTT_LOGIN,
        password=conf.MQTT_PASS,
        target_topic=conf.MQTT_TOPIC,
    )
    incoming_queue = RedisMessageQueue(
        host=conf.REDIS_HOST, port=conf.REDIS_PORT, queue=conf.REDIS_QUEUE
    )

    async with mqtt_pool as pool, incoming_queue as bridge:
        while True:
            msg = await bridge.pop()
            await pool.send(msg)


if __name__ == '__main__':
    logger.info('Sender starts wake up')
    asyncio.run(main())
