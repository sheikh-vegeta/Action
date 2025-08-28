from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.agent import Agent

class AgentRepository(ABC):
    @abstractmethod
    async def save(self, agent: Agent) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, agent_id: str) -> Optional[Agent]:
        pass
