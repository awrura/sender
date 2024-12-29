import asyncio
from asyncio import Queue

from cnpool.connection import ConnectionConfg
from cnpool.connection import MqttConnection
from cnpool.transport import PutOnlyQueue


class Sender:
    def __init__(self, queue: PutOnlyQueue):
        self._queue = queue

    async def send(self, payload):
        """
        Положить сообщение для отправки в очередь ожидаюзщих отправки сообщений
        """

        await self._queue.put(payload)


class ConnectionPool:
    def __init__(
        self,
        hostname: str,
        port: int,
        login: str,
        password: str,
        target_topic: str,
        workers: int = 4,
        max_queue_size=None,
    ):
        """
        Пул подключений

        :param workers: Количество соединений с брокером
        :param max_queue_size: Максимальный размер ожидающих сообщений
        """

        max_queue_size = max_queue_size or workers * 1024
        connection_config = ConnectionConfg(
            hostname, port, login, password, target_topic
        )

        self._queue = Queue(maxsize=workers * 1024)
        self._active_connections = []
        self._connections = [
            MqttConnection(conf=connection_config) for _ in range(workers)
        ]

    async def __aenter__(self):
        self._active_connections = [
            asyncio.create_task(conn.listen(self._queue)) for conn in self._connections
        ]
        return Sender(queue=self._queue)  # pyright: ignore[reportArgumentType]

    async def __aexit__(self, exc_type, exc, tb):
        map(lambda task: task.cancel(), self._active_connections)
