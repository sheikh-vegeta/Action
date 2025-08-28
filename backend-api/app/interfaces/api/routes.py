from fastapi import APIRouter, HTTPException, Body
from sse_starlette.sse import EventSourceResponse
from app.application.services import SessionService
from app.domain.models import Session, SessionID, Message
import asyncio

app = APIRouter()

session_service = SessionService()

@app.post("/sessions/", response_model=Session, status_code=201)
def create_session():
    """
    Create a new session.
    """
    return session_service.create_session()

@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: SessionID):
    """
    Get a session by its ID.
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/sessions/{session_id}/conversation")
async def post_message(session_id: SessionID, message: Message = Body(...)):
    """
    Post a message to a session and get a streamed response.
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=44, detail="Session not found")

    # Add user message to conversation
    session_service.add_message_to_conversation(session_id, message)

    async def event_generator():
        # This is a placeholder for the actual conversation logic
        # which will involve calling the OpenAI service.
        yield {
            "event": "message",
            "data": '{"role": "assistant", "content": "This is a streamed response."}'
        }
        await asyncio.sleep(0.1) # Simulate delay
        yield {
            "event": "message",
            "data": '{"role": "assistant", "content": "It is still streaming."}'
        }
        await asyncio.sleep(0.1) # Simulate delay
        yield {
            "event": "end",
            "data": ""
        }


    return EventSourceResponse(event_generator())
