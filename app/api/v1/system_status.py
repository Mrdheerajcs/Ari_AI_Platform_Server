from fastapi import APIRouter

router = APIRouter()

@router.get("/system-status")
def system_status():
    return {
        "chat": True,
        "history": True,
        "pdf_upload": True,
        "pdf_search": True,
        "database_engine": True,
        "global_kb": True,
        "llm": True
    }