from fastapi import APIRouter, Depends

from app.core.security import authenticate_api

from app.services.question_generator_service import (
    generate_suggested_questions
)

router = APIRouter()


@router.get(
    "/projects/{project_id}/suggested-questions"
)
def get_suggested_questions(
    project_id: str,
    user=Depends(authenticate_api)
):

    return {
        "status": "success",
        "project_id": project_id,
        "questions": generate_suggested_questions(
            project_id
        )
    }