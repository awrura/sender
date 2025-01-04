import asyncio
from functools import wraps
from typing import Type


def arecnct(
    msg: str,
    on_error: tuple[Type[Exception]],
    start_delay: int = 2,
):
    def safe_connect(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = start_delay
            while True:
                try:
                    await func(*args, **kwargs)
                except on_error:
                    print(f'{msg}. Retry after {current_delay}')
                    await asyncio.sleep(current_delay)
                    current_delay *= 2

        return wrapper

    return safe_connect
