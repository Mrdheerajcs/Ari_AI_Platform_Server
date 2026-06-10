from fastapi import APIRouter, Depends

from app.core.security import authenticate_api
from app.schemas.chat import ChatRequest

from app.services.security_service import mask_sensitive_data

from app.engines.intent_detection import detect_intent
from app.engines.context_builder import build_context
from app.engines.llm import generate_answer
from app.engines.database_intel import get_database_answer

from app.services.global_kb_service import get_global_answer
from app.services.project_service import validate_project
from app.services.role_service import validate_role
from app.services.rule_service import is_source_allowed
from app.services.chat_history_service import save_chat
from app.services.document_service import search_documents

router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    user=Depends(authenticate_api)
):

    # Project Validation
    if not validate_project(request.project_id):
        return {
            "status": "error",
            "message": "Invalid or inactive project"
        }

    # Role Validation
    if not validate_role(request.role):
        return {
            "status": "error",
            "message": "Invalid role"
        }

    # Intent Detection
    intent = detect_intent(request.question)

    # Rule Engine
    if not is_source_allowed(request.role, intent):
        return {
            "status": "error",
            "message": f"Access denied for {intent}"
        }

    # Combined AI Chatbot

    db_data = get_database_answer(
        request.project_id,
        request.question
    )

    pdf_data = search_documents(
        request.project_id,
        request.question
    )

    kb_data = get_global_answer(
        request.question
    )

    if db_data is None:
        db_data = ""

    if pdf_data is None:
        pdf_data = ""

    if kb_data is None:
        kb_data = ""

    data = f"""
DATABASE:
{db_data}

PDF:
{pdf_data}

GLOBAL:
{kb_data}
"""

    # Security Layer
    data = mask_sensitive_data(data)

    # Context Builder
    context = build_context(
        "combined",
        data
    )

    # LLM Layer
    response = generate_answer(
        request.question,
        context
    )

    # Save Chat History
    save_chat(
        request.user_id,
        request.question,
        response["answer"]
    )

    return response