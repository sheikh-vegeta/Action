from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.domain.models.agent import Agent
from app.domain.repositories.agent_repository import AgentRepository

class MongoAgentRepository(AgentRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.get_database("agent_db").get_collection("agents")

    async def save(self, agent: Agent) -> None:
        await self.collection.update_one(
            {"id": agent.id},
            {"$set": agent.model_dump()},
            upsert=True
        )

    async def find_by_id(self, agent_id: str) -> Optional[Agent]:
        data = await self.collection.find_one({"id": agent_id})
        return Agent(**data) if data else None
