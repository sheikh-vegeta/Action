import requests
from fastapi import APIRouter, Depends, HTTPException

from app.application.services import SessionService
from app.domain.models import User, SessionID
from .routes import get_current_user

# --- Environment Variables ---
TOOL_API_PORT = 8081

router = APIRouter()
session_service = SessionService()

def get_sandbox_hostname(session_id: SessionID, current_user: User) -> str:
    """Dependency to get session and sandbox hostname, and verify ownership."""
    session = session_service.get_session(session_id)
    if not session or session.owner_id != current_user.username:
        raise HTTPException(status_code=404, detail="Session not found or not owned by user")
    if not session.sandbox_id:
        raise HTTPException(status_code=404, detail="Sandbox not found for this session")
    return session.sandbox_id

@router.get("/{session_id}/files/")
def proxy_list_files(path: str = ".", hostname: str = Depends(get_sandbox_hostname)):
    """Proxy to list files in the sandbox."""
    try:
        response = requests.get(f"http://{hostname}:{TOOL_API_PORT}/files/", params={"path": path})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to tool API: {e}")

@router.get("/{session_id}/files/{filepath:path}")
def proxy_read_file(filepath: str, hostname: str = Depends(get_sandbox_hostname)):
    """Proxy to read a file in the sandbox."""
    try:
        response = requests.get(f"http://{hostname}:{TOOL_API_PORT}/files/{filepath}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to tool API: {e}")

@router.post("/{session_id}/shell/")
def proxy_run_shell(command: str, hostname: str = Depends(get_sandbox_hostname)):
    """Proxy to run a shell command in the sandbox."""
    try:
        response = requests.post(f"http://{hostname}:{TOOL_API_PORT}/shell/", params={"command": command})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to tool API: {e}")

@router.get("/{session_id}/search/")
def proxy_search(query: str, hostname: str = Depends(get_sandbox_hostname)):
    """Proxy to perform a web search in the sandbox."""
    try:
        response = requests.get(f"http://{hostname}:{TOOL_API_PORT}/search/", params={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to tool API: {e}")
