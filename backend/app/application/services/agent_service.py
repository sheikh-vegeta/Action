from __future__ import annotations

from typing import AsyncGenerator, Dict
from ...domain.models.session import Session, Message


class AgentService:
    """Minimal in-memory agent service.

    - Manages sessions in memory
    - Echoes messages as a simple assistant reply via an async generator
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}

    async def create_session(self, user_id: str) -> Session:
        session = Session(user_id=user_id)
        self._sessions[session.id] = session
        return session

    async def chat(self, session_id: str, user_id: str, message: str) -> AsyncGenerator[Message, None]:
        session = self._sessions.get(session_id)
        if session is None:
            # Auto-create if session is missing for robustness
            session = await self.create_session(user_id=user_id)
        # Record user message
        session.history.append(Message(role="user", content=message))
        # Produce a simple assistant response
        yield Message(role="assistant", content=f"Echo: {message}")
