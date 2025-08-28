from typing import Dict
from app.domain.models import Session, SessionID, Message

# In-memory storage for sessions.
# In a real application, this would be a database.
_sessions: Dict[SessionID, Session] = {}


class SessionService:
    """
    Service for managing sessions.
    """

    def create_session(self) -> Session:
        """
        Creates a new session and stores it.
        """
        session = Session()
        _sessions[session.id] = session
        return session

    def get_session(self, session_id: SessionID) -> Session | None:
        """
        Retrieves a session by its ID.
        """
        return _sessions.get(session_id)

    def add_message_to_conversation(
        self, session_id: SessionID, message: Message
    ) -> Session | None:
        """
        Adds a message to the conversation of a session.
        """
        session = self.get_session(session_id)
        if session:
            session.conversation.messages.append(message)
            return session
        return None
