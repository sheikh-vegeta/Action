from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum

class SessionStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    status: SessionStatus = SessionStatus.RUNNING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    history: List[Message] = []
    sandbox_id: Optional[str] = None
    vnc_url: Optional[str] = None
