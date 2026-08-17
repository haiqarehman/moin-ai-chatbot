from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.config import settings


app = FastAPI(
    title="MoinSystems AI Public Website Chatbot",
    version="0.1.0",
)


app.include_router(
    health_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "MoinSystems AI Chatbot API is running",
        "environment": settings.app_env,
    }