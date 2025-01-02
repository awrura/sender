import logging
import uuid
from dataclasses import dataclass
from logging import Logger

import aiomqtt
from cnpool.transport import ReadOnlyQueue


logger = logging.getLogger(__name__)


@dataclass
class ConnectionConfg:
    HOST: str
    PORT: int
    LOGIN: str
    PASS: str
    TOPIC: str


class MqttConnection:
    """
    Соединение с MQTT брокером

    Ожидает сообщений из очереди, сериализует их и отправляет в брокер
    """

    def __init__(self, conf: ConnectionConfg, logger: Logger | None = None):
        """
        Инициализация соединения

        На данном этапе соединение с брокером не устанавливается
        А задается только его конфигурация
        """

        self._conf = conf
        self._uuid = uuid.uuid4()
        self._logger = logger or logging.getLogger(__name__)

    async def listen(self, queue: ReadOnlyQueue):
        """
        Прослушивание очереди и отправка сообщений в брокер

        Устанавливает соединение с брокером
        Начинает неблокирующее ожидание сообщения из очереди
        При получении сообщения сериализует его и отправляет в брокер
        """

        self._logger.debug(f'Connection({self._uuid}) begins')
        async with aiomqtt.Client(
            hostname=self._conf.HOST,
            port=self._conf.PORT,
            username=self._conf.LOGIN,
            password=self._conf.PASS,
        ) as client:
            self._logger.info(f'Connection({self._uuid}) success')
            while True:
                payload = await queue.get()
                await client.publish(topic=self._conf.TOPIC, payload=payload)
                self._logger.info(
                    f"Connection({self._uuid}) sent message into '{self._conf.TOPIC}' topic"
                )
