from fastapi import APIRouter
from app.services.chat_history_service import get_history

router = APIRouter()

@router.get("/history")
def history():
    return get_history()