from fastapi import APIRouter, HTTPException, Body, Depends, Query
from sse_starlette.sse import EventSourceResponse
from app.application.services import SessionService
from app.application.services.auth import AuthService
from app.application.services.agent import AgentService
from app.domain.models import Session, SessionID, Message, User
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

app = APIRouter()

session_service = SessionService()
auth_service = AuthService()
agent_service = AgentService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    token_query: Optional[str] = Query(None, alias="token")
):
    """
    Dependency to get the current user from a token in the Authorization header or query string.
    """
    auth_token = token or token_query
    if not auth_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = auth_service.get_current_user(auth_token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/sessions/", response_model=Session, status_code=201)
def create_session(current_user: User = Depends(get_current_user)):
    """
    Create a new session for the authenticated user.
    """
    return session_service.create_session(owner_id=current_user.username)

@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: SessionID, current_user: User = Depends(get_current_user)):
    """
    Get a session by its ID.
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/sessions/{session_id}/conversation")
async def post_message(session_id: SessionID, message: Message = Body(...), current_user: User = Depends(get_current_user)):
    """
    Post a message to a session and get a streamed response from the agent.
    """
    session = session_service.get_session(session_id)
    if not session or session.owner_id != current_user.username:
        raise HTTPException(status_code=404, detail="Session not found or not owned by user")

    session_service.add_message_to_conversation(session_id, message)
    updated_session = session_service.get_session(session_id)

    async def event_generator():
        async for event in agent_service.process_message(updated_session, message):
            yield {"data": event}

    return EventSourceResponse(event_generator())
