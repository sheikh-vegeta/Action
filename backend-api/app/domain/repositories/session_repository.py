from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.session import Session

class SessionRepository(ABC):
    @abstractmethod
    async def save(self, session: Session) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, session_id: str) -> Optional[Session]:
        pass

    @abstractmethod
    async def find_by_id_and_user_id(self, session_id: str, user_id: str) -> Optional[Session]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Session]:
        pass

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        pass

    @abstractmethod
    async def update_unread_message_count(self, session_id: str, count: int) -> None:
        pass
