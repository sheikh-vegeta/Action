from pydantic import BaseModel
from typing import Any

class AgentEvent(BaseModel):
    event: str
    data: Any
