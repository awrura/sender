from typing import Protocol


class EndlessMessageStream(Protocol):
    """
    Непрерывный поток сообщений.
    Позволяет асинхронно итерироваться по набору сообщений
    Если сообщений в потоке нет, то итерирование не прерывается, а дожидается новых сообщений
    """

    def __aiter__(self):
        raise NotImplementedError()

    async def __anext__(self):
        raise NotImplementedError()
