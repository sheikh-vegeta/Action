from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model_name: str
    temperature: float
    max_tokens: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
