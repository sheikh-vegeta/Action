import os
import requests
import secrets
from pymongo import MongoClient
from app.domain.models import Session, SessionID, Message, Conversation
from typing import Optional

# --- Environment Variables ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
SANDBOX_MANAGER_URL = os.environ.get("SANDBOX_MANAGER_URL", "http://sandbox-manager:8080")


class SessionService:
    """
    Service for managing sessions using MongoDB and interacting with the Sandbox Manager.
    """

    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.get_database("agent_db")
        self.sessions = self.db.get_collection("sessions")

    def create_session(self, owner_id: str) -> Optional[Session]:
        """
        Creates a new session, triggers sandbox creation, and stores it in MongoDB.
        """
        # 1. Request a new sandbox from the sandbox-manager
        try:
            response = requests.post(f"{SANDBOX_MANAGER_URL}/sandboxes/")
            response.raise_for_status()
            sandbox_data = response.json()
            sandbox_id = sandbox_data.get("id")
        except requests.exceptions.RequestException as e:
            print(f"Error creating sandbox: {e}")
            return None

        # 2. Create the session object
        session = Session(
            owner_id=owner_id,
            sandbox_id=sandbox_id,
            vnc_ticket=secrets.token_urlsafe(16) # Generate a secure random ticket
        )

        # 3. Store session in MongoDB
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

        session.conversation.messages.append(message)
        self.sessions.update_one(
            {"id": session_id},
            {"$set": {"conversation": session.conversation.model_dump()}}
        )
        return session

    def validate_vnc_ticket(self, session_id: SessionID, ticket: str) -> bool:
        """
        Validates and consumes a VNC ticket.
        """
        session = self.get_session(session_id)
        if session and session.vnc_ticket and session.vnc_ticket == ticket:
            # Consume the ticket after use
            self.sessions.update_one(
                {"id": session_id},
                {"$set": {"vnc_ticket": None}}
            )
            return True
        return False
