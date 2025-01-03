from typing import Any
from typing import Protocol


class PutOnlyQueue(Protocol):
    """
    Очередь сообщений, только на запись элементов

    Позволяет асинхронно положить в очередь значение.
    Если очередь переполнена, то будет ожидать освобождения места
    """

    async def put(self, msg: Any):
        raise NotImplementedError()


class ReadOnlyQueue(Protocol):
    """
    Очередь сообщений, только на получение элементов

    Позволяет асинхронно получить (выдернуть) сообщение из очереди
    Если два клиента слушают одну и ту же очередь, сообщение доставляется только однму из них
    Если сообщений в очереди нет, то клиент ожидает его
    """

    async def get(self) -> Any:
        raise NotImplementedError()
