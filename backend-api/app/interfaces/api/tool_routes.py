from fastapi import APIRouter, Depends
from app.application.services.agent_service import AgentService
from app.dependencies import get_agent_service
from app.interfaces.schemas.session import ShellViewResponse
from app.interfaces.schemas.file import FileViewResponse
from typing import List
from app.domain.models.file import FileInfo


router = APIRouter()

@router.get("/{session_id}/shell/{shell_session_id}", response_model=ShellViewResponse)
async def view_shell(
    session_id: str,
    shell_session_id: str,
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.shell_view(session_id, shell_session_id, user_id)

@router.get("/{session_id}/files/{file_path:path}", response_model=FileViewResponse)
async def view_file(
    session_id: str,
    file_path: str,
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.file_view(session_id, file_path, user_id)

@router.get("/{session_id}/files/", response_model=List[FileInfo])
async def list_files(
    session_id: str,
    user_id: str = "default_user",
    agent_service: AgentService = Depends(get_agent_service)
):
    return await agent_service.get_session_files(session_id, user_id)
