from fastapi import FastAPI
from .dependencies import client
from .interfaces.api import routes, auth_routes, websocket_routes, tool_routes, vnc_routes

app = FastAPI(
    title="Intelligent Conversation Agent API",
    description="Main API for the agent.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    # This is where you would connect to the database
    pass

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

app.include_router(routes.router, prefix="/api", tags=["api"])
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(tool_routes.router, prefix="/tools", tags=["tools"])
app.include_router(vnc_routes.router, prefix="/vnc", tags=["vnc"])
