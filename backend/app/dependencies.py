import os
from motor.motor_asyncio import AsyncIOMotorClient
from .infrastructure.repositories.mongo_session_repository import MongoSessionRepository
from .infrastructure.repositories.mongo_agent_repository import MongoAgentRepository
from .application.services.agent_service import AgentService
from .core.llm_factory import get_llm

# --- Dependency Injection Setup ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/")
client = AsyncIOMotorClient(MONGO_URI)

def get_session_repository() -> MongoSessionRepository:
    return MongoSessionRepository(client)

def get_agent_repository() -> MongoAgentRepository:
    return MongoAgentRepository(client)

def get_agent_service() -> AgentService:
    # In a real app, the other dependencies would be implemented and injected here
    return AgentService(
        llm=get_llm(),
        agent_repository=get_agent_repository(),
        session_repository=get_session_repository(),
        # The rest are placeholders until implemented
        sandbox_cls=None,
        task_cls=None,
        json_parser=None,
        file_storage=None,
        mcp_repository=None,
        search_engine=None
    )
