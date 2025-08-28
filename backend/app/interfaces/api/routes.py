from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from ...application.services.agent_service import AgentService
from ...dependencies import get_agent_service
from ...domain.models.session import Session

router = APIRouter()

@router.post("/sessions/", response_model=Session)
async def create_session(
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.create_session(user_id="default_user")

@router.post("/sessions/{session_id}/chat")
async def chat(
    session_id: str,
    message: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    async def event_stream():
        async for event in agent_service.chat(session_id, "default_user", message):
            yield {"data": event.model_dump_json()}

    return EventSourceResponse(event_stream())
