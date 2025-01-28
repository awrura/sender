from asyncio import Queue
from typing import Protocol
from typing import TypedDict


class Message(TypedDict):
    topic: str
    payload: bytes


class PutOnlyQueue(Protocol):
    """
    Очередь сообщений, только на запись элементов

    Позволяет асинхронно положить в очередь значение.
    Если очередь переполнена, то будет ожидать освобождения места
    """

    async def put(self, msg: Message):
        raise NotImplementedError()


class ReadOnlyQueue(Protocol):
    """
    Очередь сообщений, только на получение элементов

    Позволяет асинхронно получить (выдернуть) сообщение из очереди
    Если два клиента слушают одну и ту же очередь, сообщение доставляется только однму из них
    Если сообщений в очереди нет, то клиент ожидает его
    """

    async def get(self) -> Message:
        raise NotImplementedError()


class MessageQueue(PutOnlyQueue, ReadOnlyQueue):
    """
    Очередь сообщений

    Реализация очереди сообщений, построенная на asyncio.Queue
    Проксирует вызовы в api получения и вставки элемента в очередь
    При получении элемента из очереди автоматически
    уменьшает счетчик незавершенных задач в asyncio.Queue на 1
    """

    def __init__(self, queue: Queue):
        self._queue = queue

    async def put(self, msg: Message):
        await self._queue.put(msg)

    async def get(self) -> Message:
        msg = await self._queue.get()
        self._queue.task_done()
        return msg
