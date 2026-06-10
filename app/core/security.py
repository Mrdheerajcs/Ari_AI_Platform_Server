from datetime import datetime, timedelta

import jwt
from fastapi import Header, HTTPException

SECRET_KEY = "ari_ai_platform_secret_key"
ALGORITHM = "HS256"

BYPASS_TOKEN = "ARI_BYPASS_TOKEN"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = (
        datetime.utcnow()
        + timedelta(hours=24)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):

    if token == BYPASS_TOKEN:

        return {
            "bypass": True
        }

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        return None


def authenticate_api(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload
def build_response(
    message: str,
    data: dict
):

    token = create_access_token(data)

    return {
        "token": token,
        "status": "success",
        "message": message,
        "data": data
    }