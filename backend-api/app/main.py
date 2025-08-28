import uvicorn
from fastapi import FastAPI
from app.interfaces.api.routes import app as api_router
from .interfaces.api.auth_routes import router as auth_router
from .interfaces.api.websocket_routes import router as websocket_router

app = FastAPI(
    title="Intelligent Conversation Agent API",
    description="Main API for the agent.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(websocket_router, prefix="/ws", tags=["websockets"])

from .interfaces.api.tool_routes import router as tool_router
app.include_router(tool_router, prefix="/tools", tags=["tools"])

from .interfaces.api.vnc_routes import router as vnc_router
app.include_router(vnc_router, prefix="/vnc", tags=["vnc"])
