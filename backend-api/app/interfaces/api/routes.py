from fastapi import APIRouter, Depends, Body
from sse_starlette.sse import EventSourceResponse
from app.application.services.agent_service import AgentService
from app.dependencies import get_agent_service
from app.domain.models.session import Session
from app.domain.models.event import AgentEvent
from typing import List, Optional

router = APIRouter()

@router.post("/sessions/", response_model=Session, status_code=201)
async def create_session(
    user_id: str = "default_user", # In a real app, this would come from an auth dependency
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.create_session(user_id)

@router.get("/sessions/{session_id}", response_model=Session)
async def get_session(
    session_id: str,
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.get_session(session_id, user_id)

@router.get("/sessions/", response_model=List[Session])
async def get_all_sessions(
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.get_all_sessions(user_id)

@router.post("/sessions/{session_id}/conversation")
async def post_message(
    session_id: str,
    message: str = Body(..., embed=True),
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    async def event_generator():
        async for event in agent_service.chat(session_id, user_id, message):
            yield {"data": event.model_dump_json()}

    return EventSourceResponse(event_generator())
