import uvicorn
from fastapi import FastAPI
from app.interfaces.api.routes import app as api_router
from .interfaces.api.auth_routes import router as auth_router

app = FastAPI(
    title="Intelligent Conversation Agent API",
    description="Main API for the agent.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
