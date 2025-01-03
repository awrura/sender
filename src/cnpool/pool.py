import asyncio
import logging
from asyncio import Queue
from logging import Logger

from cnpool.connection import ConnectionConfg
from cnpool.connection import MqttConnection
from cnpool.transport import PutOnlyQueue


class Sender:
    def __init__(self, queue: PutOnlyQueue, logger: Logger | None = None):
        self._queue = queue
        self._logger = logger or logging.getLogger(__name__)

    async def send(self, payload):
        """
        Положить сообщение для отправки в очередь ожидаюзщих отправки сообщений
        """

        await self._queue.put(payload)
        self._logger.debug('Message put in queue')


class MqttConnectionPool:
    def __init__(
        self,
        hostname: str,
        port: int,
        login: str,
        password: str,
        target_topic: str,
        logger: Logger | None = None,
        workers: int = 4,
        max_queue_size=None,
    ):
        """
        Пул подключений к MQTT брокеру.

        Позволяет создать несколько подключений к брокеру
        и отправлять в него сообщение, используя свободные подключения

        Все созданные соединения слушают одну очередь, при этом одно сообщение может
        обработать (взять из очереди) только одно соединение.
        При отправке сообщения оно помещается в очередь и его извлекает одно из
        свободных соединений.

        :param target_topic: Название MQTT топика в который будут отправляться сообщения
        :param workers: Количество соединений с брокером
        :param max_queue_size: Максимальный размер ожидающих сообщений. По умолчанию = workers * 1024
        """

        max_queue_size = max_queue_size or workers * 1024
        connection_config = ConnectionConfg(
            hostname, port, login, password, target_topic
        )

        self._queue = Queue(maxsize=max_queue_size)
        self._logger = logger or logging.getLogger(__name__)
        self._active_connections = []
        self._connections = [
            MqttConnection(conf=connection_config, logger=self._logger)
            for _ in range(workers)
        ]

    async def __aenter__(self):
        self._active_connections = [
            asyncio.create_task(conn.listen(self._queue)) for conn in self._connections
        ]
        self._logger.debug(
            f'Enter in pool manager success. Num connections: {len(self._connections)}'
        )
        return Sender(queue=self._queue)  # pyright: ignore[reportArgumentType]

    async def __aexit__(self, exc_type, exc, tb):
        map(lambda task: task.cancel(), self._active_connections)
        self._logger.debug('Exit from pool manager success')
