from pydantic import BaseModel, Field
from typing import List, Literal, NewType
import uuid

# Using NewType for stricter type checking of IDs
SessionID = NewType("SessionID", str)
ConversationID = NewType("ConversationID", str)

class Message(BaseModel):
    """
    Represents a single message in a conversation.
    """
    role: Literal["user", "assistant", "system"]
    content: str

class Conversation(BaseModel):
    """
    Represents a conversation, which is a list of messages.
    """
    id: ConversationID = Field(default_factory=lambda: ConversationID(str(uuid.uuid4())))
    messages: List[Message] = []

class Session(BaseModel):
    """
    Represents a user session, containing a conversation.
    """
    id: SessionID = Field(default_factory=lambda: SessionID(str(uuid.uuid4())))
    conversation: Conversation = Field(default_factory=Conversation)
    owner_id: str  # To associate session with a user
    sandbox_id: str | None = None # To link to a running sandbox
    vnc_ticket: str | None = None # Short-lived ticket for VNC access


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
