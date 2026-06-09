from fastapi import FastAPI

from app.api.v1.documents import router as documents_router
from app.api.v1.chat import router as chat_router
from app.api.v1.history import router as history_router
from app.api.v1.system_status import router as system_status_router
from app.api.v1.project_config import router as config_router
from app.api.v1.projects import router as project_router

app = FastAPI(
    title="ARI AI Platform",
    version="1.0.0"
)

# Chat
app.include_router(
    chat_router,
    prefix="/api/v1",
    tags=["Chat"]
)

# History
app.include_router(
    history_router,
    prefix="/api/v1",
    tags=["History"]
)

# Documents
app.include_router(
    documents_router,
    prefix="/api/v1",
    tags=["Documents"]
)

# System Status
app.include_router(
    system_status_router,
    prefix="/api/v1",
    tags=["System"]
)

# Projects
app.include_router(
    project_router,
    prefix="/api/v1",
    tags=["Projects"]
)

# Project Config
app.include_router(
    config_router,
    prefix="/api/v1",
    tags=["Project Config"]
)


@app.get("/")
def root():
    return {
        "message": "ARI AI Platform Running",
        "status": "success"
    }