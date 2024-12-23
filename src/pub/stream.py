from typing import Protocol


class MessageStream(Protocol):
    def __aiter__(self):
        raise NotImplementedError('It is a abstract realisation')
