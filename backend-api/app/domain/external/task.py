from abc import ABC, abstractmethod
from typing import Any

class Task(ABC):
    @abstractmethod
    async def run(self) -> Any:
        pass
