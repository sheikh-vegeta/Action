from pydantic import BaseModel

class ShellViewResponse(BaseModel):
    output: str
