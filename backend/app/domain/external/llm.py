from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLM(ABC):
    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        pass
