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
