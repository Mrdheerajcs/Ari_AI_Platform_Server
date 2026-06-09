from datetime import datetime
import bcrypt
from sqlalchemy import text
from app.core.database import engine


def generate_password(email: str):

    email_name = email.split("@")[0]

    first_three = email_name[:3]

    last_three = email_name[-3:]

    raw_password = first_three + last_three

    encrypted_password = bcrypt.hashpw(
        raw_password.encode(),
        bcrypt.gensalt()
    ).decode()

    return raw_password, encrypted_password


def create_project(
    name: str,
    description: str,
    email: str,
    enable_db: bool
):

    year = datetime.now().strftime("%y")

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT project_id
                FROM projects
                WHERE project_id LIKE :prefix
                ORDER BY project_id DESC
                LIMIT 1
                """
            ),
            {
                "prefix": f"ARI{year}-%"
            }
        ).fetchone()

    if result:

        last_project_id = result[0]

        last_number = int(
            last_project_id.split("-")[1]
        )

        next_number = last_number + 1

    else:

        next_number = 1

    project_id = f"ARI{year}-{next_number:03}"

    raw_password, encrypted_password = generate_password(
        email
    )

    with engine.begin() as conn:

        conn.execute(
            text(
                """
                INSERT INTO projects
                (
                    project_id,
                    project_name,
                    description,
                    status,
                    enable_db,
                    email,
                    role,
                    password
                )
                VALUES
                (
                    :project_id,
                    :project_name,
                    :description,
                    'active',
                    :enable_db,
                    :email,
                    'user',
                    :password
                )
                """
            ),
            {
                "project_id": project_id,
                "project_name": name,
                "description": description,
                "enable_db": enable_db,
                "email": email,
                "password": encrypted_password
            }
        )

    return {
        "project_id": project_id,
        "name": name,
        "description": description,
        "email": email,
        "role": "user",
        # "generated_password": raw_password,
        "generated_password": encrypted_password,
        "enable_db": enable_db,
        "active": True
    }


def get_projects():

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    project_id,
                    project_name,
                    description,
                    email,
                    role,
                    enable_db,
                    status
                FROM projects
                ORDER BY id
                """
            )
        )

        rows = []

        for row in result:

            rows.append(
                dict(row._mapping)
            )

        return rows


def get_project(project_id: str):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    project_id,
                    project_name,
                    description,
                    email,
                    role,
                    enable_db,
                    status
                FROM projects
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id
            }
        ).fetchone()

        if not result:
            return {
                "status": "error",
                "message": "Project not found"
            }

        return dict(result._mapping)


def update_project(
    project_id: str,
    name: str,
    description: str,
    email: str,
    enable_db: bool
):

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET
                    project_name = :name,
                    description = :description,
                    email = :email,
                    enable_db = :enable_db
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id,
                "name": name,
                "description": description,
                "email": email,
                "enable_db": enable_db
            }
        )

        if result.rowcount == 0:
            return {
                "status": "error",
                "message": "Project not found"
            }

    return get_project(project_id)
def activate_project(project_id: str):

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET status = 'active'
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id
            }
        )

        if result.rowcount == 0:
            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": "Project activated successfully"
    }


def deactivate_project(project_id: str):

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET status = 'inactive'
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id
            }
        )

        if result.rowcount == 0:
            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": "Project deactivated successfully"
    }


def maintenance_project(project_id: str):

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET status = 'maintenance'
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id
            }
        )

        if result.rowcount == 0:
            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": "Project moved to maintenance mode"
    }


def delete_project(project_id: str):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                DELETE FROM projects
                WHERE project_id = :project_id
            """),
            {
                "project_id": project_id
            }
        )

        if result.rowcount == 0:
            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": "Project deleted successfully"
    }