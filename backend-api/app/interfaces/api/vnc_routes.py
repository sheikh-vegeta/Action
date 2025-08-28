import secrets
from fastapi import APIRouter, Depends, HTTPException

from app.application.services import SessionService
from app.domain.models import User, SessionID
from .routes import get_current_user

router = APIRouter()
session_service = SessionService()

@router.get("/{session_id}/vnc-ticket")
def get_vnc_ticket(session_id: SessionID, current_user: User = Depends(get_current_user)):
    """
    Generates and returns a new one-time VNC access ticket for a session.
    """
    session = session_service.get_session(session_id)
    if not session or session.owner_id != current_user.username:
        raise HTTPException(status_code=404, detail="Session not found or not owned by user")

    # Generate and save a new ticket
    ticket = secrets.token_urlsafe(16)
    session_service.sessions.update_one(
        {"id": session.id},
        {"$set": {"vnc_ticket": ticket}}
    )

    return {"ticket": ticket}
