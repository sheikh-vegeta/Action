from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLM(ABC):
    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]]) -> Any:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def temperature(self) -> float:
        pass

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        pass
