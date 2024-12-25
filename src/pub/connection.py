from typing import Protocol

from pub.stream import EndlessMessageStream


class StreamConnection(Protocol):
    """
    Соединение прослушивающее поток данных
    При наличии сообщения в потоке извлекает его и отправляет получателю
    """

    async def listen(self, stream: EndlessMessageStream):
        """
        Начать прослушивать поток данных.
        При извлечении сообщения отправляет его получателю
        """

        raise NotImplementedError()
