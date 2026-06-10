import bcrypt

from sqlalchemy import text

from app.core.database import engine
from app.core.security import build_response


def login_user(
    email: str,
    password: str
):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    id,
                    project_id,
                    email,
                    password,
                    role
                FROM projects
                WHERE email = :email
                """
            ),
            {
                "email": email
            }
        ).fetchone()

    if not result:

        return {
            "status": "error",
            "message": "Invalid email or password"
        }

    stored_password = result.password

    if not stored_password:

        return {
            "status": "error",
            "message": "Password not configured for this project"
        }

    if not bcrypt.checkpw(
        password.encode(),
        stored_password.encode()
    ):

        return {
            "status": "error",
            "message": "Invalid email or password"
        }

    return build_response(
        "Login successful",
        {
            "id": result.id,
            "project_id": result.project_id,
            "email": result.email,
            "role": result.role
        }
    )