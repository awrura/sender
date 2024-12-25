import asyncio

import aiomqtt
from pub.connection import StreamConnection
from pub.stream import EndlessMessageStream
from pydantic_settings import BaseSettings


class MqttConnectionConfg(BaseSettings):
    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_LOGIN: str
    MQTT_PASS: str
    MQTT_TOPIC: str


class MqttConnection(StreamConnection):
    """
    Соединение с MQTT брокером

    Позволяет создать соединение с MQTT брокером,
    и прослушивания поток данных, отправлять данные в него
    """

    def __init__(self, conf: MqttConnectionConfg):
        """
        Инициализация соединения

        На данном этапе соединение с брокером не устанавливается
        А задается только конфигурация соединения
        """

        self._conf = conf

    async def listen(self, stream: EndlessMessageStream):
        """
        Прослушивание потока данных и отправка сообщений в MQTT брокер

        Устанавливает соединение с MQTT брокером
        Начинает прослушивание потока данных, пока он не закончится (а он бесконечный)
        При получении сообщения сериализует его и отправляет в брокер
        """

        async with aiomqtt.Client(
            hostname=self._conf.MQTT_HOST,
            port=self._conf.MQTT_PORT,
            username=self._conf.MQTT_LOGIN,
            password=self._conf.MQTT_PASS,
        ) as client:
            print(f'Client |{id(client)}| connected')
            async for msg in stream:
                print(f'Client |{id(client)}| sent message {msg}')
                await client.publish(
                    topic=self._conf.MQTT_TOPIC, payload=f'{id(client)} - {msg}'
                )
                await asyncio.sleep(5)
