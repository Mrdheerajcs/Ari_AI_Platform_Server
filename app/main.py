from fastapi import FastAPI
from app.api.v1.database_config import (
    router as database_config_router
)
from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router
from app.api.v1.global_documents import router as global_documents_router
from app.api.v1.chat import router as chat_router
from app.api.v1.history import router as history_router
from app.api.v1.system_status import router as system_status_router
from app.api.v1.project_config import router as config_router
from app.api.v1.projects import router as project_router
from app.api.v1.suggested_questions import (
    router as suggested_questions_router
)

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

app.include_router(
    suggested_questions_router,
    prefix="/api/v1",
    tags=["Suggested Questions"]
)

# Authentication
app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["Authentication"]
)

app.include_router(
    database_config_router,
    prefix="/api/v1",
    tags=["Database Config"]
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

# Global Documents
app.include_router(
    global_documents_router,
    prefix="/api/v1",
    tags=["Global Documents"]
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