from abc import ABC, abstractmethod
from typing import List
from app.domain.models.file import FileInfo

class FileStorage(ABC):
    @abstractmethod
    async def list_files(self, path: str) -> List[FileInfo]:
        pass

    @abstractmethod
    async def read_file(self, path: str) -> str:
        pass

    @abstractmethod
    async def write_file(self, path: str, content: str) -> None:
        pass
