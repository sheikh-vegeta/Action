from abc import ABC, abstractmethod
from typing import Any

class Sandbox(ABC):
    @classmethod
    @abstractmethod
    async def get(cls, sandbox_id: str) -> Any:
        pass

    @abstractmethod
    async def view_shell(self, session_id: str, console: bool) -> Any:
        pass

    @abstractmethod
    async def file_read(self, path: str) -> Any:
        pass

    @property
    @abstractmethod
    def vnc_url(self) -> str:
        pass
