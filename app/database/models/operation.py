from dataclasses import dataclass
from typing import List

@dataclass
class Operation:
    name: str
    priority: int
    restrictions: List[object]