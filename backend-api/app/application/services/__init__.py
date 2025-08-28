import os
from pymongo import MongoClient
from app.domain.models import Session, SessionID, Message, Conversation
from typing import Optional

class SessionService:
    """
    Service for managing sessions using MongoDB.
    """

    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database("agent_db")
        self.sessions = self.db.get_collection("sessions")

    def create_session(self) -> Session:
        """
        Creates a new session and stores it in MongoDB.
        """
        session = Session()
        self.sessions.insert_one(session.model_dump())
        return session

    def get_session(self, session_id: SessionID) -> Optional[Session]:
        """
        Retrieves a session by its ID from MongoDB.
        """
        session_data = self.sessions.find_one({"id": session_id})
        if session_data:
            return Session(**session_data)
        return None

    def add_message_to_conversation(
        self, session_id: SessionID, message: Message
    ) -> Optional[Session]:
        """
        Adds a message to the conversation of a session in MongoDB.
        """
        session = self.get_session(session_id)
        if not session:
            return None

        # Add message and update in DB
        session.conversation.messages.append(message)
        self.sessions.update_one(
            {"id": session_id},
            {"$set": {"conversation": session.conversation.model_dump()}}
        )
        return session
