import logging
import uuid
from dataclasses import dataclass
from logging import Logger

import aiomqtt
from cnpool.transport import ReadOnlyQueue
from utils.reconnect import arecnct

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

    def __init__(
        self, conf: ConnectionConfg, logger: Logger | None = None, retry_sec: int = 10
    ):
        """
        Инициализация соединения

        На данном этапе соединение с брокером не устанавливается
        А задается только его конфигурация
        """

        self._conf = conf
        self._uuid = uuid.uuid4()
        self._logger = logger or logging.getLogger(__name__)
        self._retry_sec = retry_sec

    async def listen(self, queue: ReadOnlyQueue):
        """
        Прослушивание очереди и отправка сообщений в брокер

        Устанавливает соединение с брокером
        Начинает неблокирующее ожидание сообщения из очереди
        При получении сообщения сериализует его и отправляет в брокер
        """

        self._logger.debug(f'Connection({self._uuid}) begins')
        client = aiomqtt.Client(
            hostname=self._conf.HOST,
            port=self._conf.PORT,
            username=self._conf.LOGIN,
            password=self._conf.PASS,
        )

        await self._forward_queue_messages(client, queue)

    @arecnct(msg='Connection to MQTT Broker failed', on_error=(aiomqtt.MqttError,))
    async def _forward_queue_messages(
        self, client: aiomqtt.Client, queue: ReadOnlyQueue
    ):
        """
        Пересылка сообщений из очереди MQTT брокеру

        :param client: Уже подключенный к брокеру клиент
        :param queue: Очередь из которой забирать сообщения
        """

        async with client:
            self._logger.info(f'Connection({self._uuid}) success')
            while True:
                payload = await queue.get()
                await client.publish(topic=self._conf.TOPIC, payload=payload)
                self._logger.info(
                    f"Connection({self._uuid}) sent message into '{self._conf.TOPIC}' topic"
                )
