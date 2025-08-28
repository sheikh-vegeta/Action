from fastapi import APIRouter, Depends
from app.application.services.agent_service import AgentService
from app.dependencies import get_agent_service

router = APIRouter()

@router.get("/{session_id}/vnc-url")
async def get_vnc_url(
    session_id: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    url = await agent_service.get_vnc_url(session_id)
    return {"url": url}
