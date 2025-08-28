from __future__ import annotations

from .application.services.agent_service import AgentService

# For now a single global instance is acceptable for demo/testing
_agent_service = AgentService()


def get_agent_service() -> AgentService:
    return _agent_service
