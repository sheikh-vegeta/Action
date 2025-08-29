from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from app.domain.models.session import Session
from app.domain.repositories.session_repository import SessionRepository

class MongoSessionRepository(SessionRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.get_database("agent_db").get_collection("sessions")

    async def save(self, session: Session) -> None:
        await self.collection.update_one(
            {"id": session.id},
            {"$set": session.model_dump()},
            upsert=True
        )

    async def find_by_id(self, session_id: str) -> Optional[Session]:
        data = await self.collection.find_one({"id": session_id})
        return Session(**data) if data else None

    async def find_by_user_id(self, user_id: str) -> List[Session]:
        cursor = self.collection.find({"user_id": user_id})
        return [Session(**data) async for data in cursor]

    async def delete(self, session_id: str) -> None:
        await self.collection.delete_one({"id": session_id})
