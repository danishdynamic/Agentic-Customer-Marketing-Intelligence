from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.rag import router as rag_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


app.include_router(health_router)
app.include_router(rag_router)