from abc import ABC, abstractmethod
from typing import Dict, Any

class MCPRepository(ABC):
    @abstractmethod
    def get_available_tools(self) -> Dict[str, Any]:
        pass
