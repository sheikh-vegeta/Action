import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.infrastructure.repositories.mongo_session_repository import MongoSessionRepository
from app.infrastructure.repositories.mongo_agent_repository import MongoAgentRepository
from app.infrastructure.repositories.json_mcp_repository import JsonMCPRepository
from app.application.services.agent_service import AgentService
# We will need to create concrete implementations for these external services
# For now, I will create dummy implementations here.

from app.domain.external.llm import LLM
from app.domain.external.sandbox import Sandbox
from app.domain.external.search import SearchEngine
from app.domain.external.file import FileStorage
from app.domain.external.task import Task
from app.domain.utils.json_parser import JsonParser

# --- Dummy Implementations for External Services ---
class DummyLLM(LLM):
    async def chat_completion(self, messages): return {"choices": [{"message": {"content": "dummy response"}}]}
    @property
    def model_name(self): return "dummy_model"
    @property
    def temperature(self): return 0.0
    @property
    def max_tokens(self): return 100

class DummySandbox(Sandbox):
    @classmethod
    async def get(cls, sandbox_id): return cls()
    async def view_shell(self, session_id, console): return {"success": True, "data": {"output": "dummy shell output"}}
    async def file_read(self, path): return {"success": True, "data": {"content": "dummy file content"}}
    @property
    def vnc_url(self): return "ws://dummy-vnc"

# --- Dependency Injection Setup ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = AsyncIOMotorClient(MONGO_URI)

def get_session_repository() -> MongoSessionRepository:
    return MongoSessionRepository(client)

def get_agent_repository() -> MongoAgentRepository:
    return MongoAgentRepository(client)

def get_mcp_repository() -> JsonMCPRepository:
    return JsonMCPRepository()

def get_agent_service() -> AgentService:
    # This is a simplified setup. In a real app, these would be configurable.
    return AgentService(
        llm=DummyLLM(),
        agent_repository=get_agent_repository(),
        session_repository=get_session_repository(),
        sandbox_cls=DummySandbox,
        task_cls=None, # Placeholder
        json_parser=JsonParser(),
        file_storage=None, # Placeholder
        mcp_repository=get_mcp_repository(),
        search_engine=None # Placeholder
    )
