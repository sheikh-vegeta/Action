from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .interfaces.api import routes

app = FastAPI(
    title="Intelligent Agent Backend API",
    description="Core business logic and API gateway.",
    version="1.0.0"
)

# Permissive CORS for development; tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

app.include_router(routes.router)
