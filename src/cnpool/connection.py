from dataclasses import dataclass

import aiomqtt
from cnpool.transport import ReadOnlyQueue


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

    def __init__(self, conf: ConnectionConfg):
        """
        Инициализация соединения

        На данном этапе соединение с брокером не устанавливается
        А задается только его конфигурация
        """

        self._conf = conf

    async def listen(self, queue: ReadOnlyQueue):
        """
        Прослушивание очереди и отправка сообщений в брокер

        Устанавливает соединение с брокером
        Начинает неблокирующее ожидание сообщения из очереди
        При получении сообщения сериализует его и отправляет в брокер
        """

        async with aiomqtt.Client(
            hostname=self._conf.HOST,
            port=self._conf.PORT,
            username=self._conf.LOGIN,
            password=self._conf.PASS,
        ) as client:
            print(f'Client |{id(client)}| connected')
            while True:
                payload = await queue.get()
                print(f'Client |{id(client)}| sent message {payload}')
                await client.publish(topic=self._conf.TOPIC, payload=payload)
