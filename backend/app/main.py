from fastapi import FastAPI
from .interfaces.api import routes

app = FastAPI(
    title="Intelligent Agent Backend API",
    description="Core business logic and API gateway.",
    version="1.0.0"
)

app.include_router(routes.router)
