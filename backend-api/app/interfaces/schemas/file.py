from pydantic import BaseModel

class FileViewResponse(BaseModel):
    content: str
