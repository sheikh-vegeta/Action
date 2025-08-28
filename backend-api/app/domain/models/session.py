from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum

class SessionStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    agent_id: str
    sandbox_id: Optional[str] = None
    status: SessionStatus = SessionStatus.RUNNING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    conversation: List[dict] = []
    files: List[dict] = []
    unread_message_count: int = 0
    vnc_ticket: Optional[str] = None # Keeping this from my previous implementation
