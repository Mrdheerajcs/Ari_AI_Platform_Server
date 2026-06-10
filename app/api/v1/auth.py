from fastapi import APIRouter

from app.models.login import LoginRequest

from app.services.auth_service import (
    login_user
)

router = APIRouter()


@router.post("/login")
def login(
    request: LoginRequest
):

    return login_user(
        request.email,
        request.password
    )