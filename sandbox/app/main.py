from fastapi import FastAPI
from .api.v1 import shell, file

app = FastAPI(
    title="Sandbox Utility API",
    version="1.0.0"
)

app.include_router(shell.router, prefix="/v1/shell", tags=["shell"])
app.include_router(file.router, prefix="/v1/file", tags=["file"])
