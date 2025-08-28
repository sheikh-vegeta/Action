from abc import ABC, abstractmethod
from typing import List

class SearchEngine(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[str]:
        pass
