from dataclasses import dataclass
from typing import List


@dataclass
class ParsedMessage:
    data: List[int]
    command: int
    topic: str
