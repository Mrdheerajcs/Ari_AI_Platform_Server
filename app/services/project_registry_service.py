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
                    id,
                    project_id,
                    project_name,
                    description,
                    status,
                    enable_db,
                    enable_global_kb,
                    service_start_date,
                    service_end_date,
                    subscription_tier,
                    max_queries_per_day,
                    max_storage_mb,
                    created_by,
                    created_at,
                    updated_at,
                    deleted_at,
                    email,
                    role
                FROM projects
                ORDER BY id
                """
            )
        )

        rows = []

        for row in result:

            project = dict(row._mapping)

            docs = conn.execute(
                text(
                    """
                    SELECT
                        id,
                        document_name,
                        s3_path
                    FROM project_documents
                    WHERE project_id = :project_db_id
                    ORDER BY id
                    """
                ),
                {
                    "project_db_id": row.id
                }
            ).fetchall()

            project["docPath"] = []

            for doc in docs:

                project["docPath"].append(
                    {
                        "docId": doc.id,
                        "docName": doc.document_name,
                        "docpath": doc.s3_path
                    }
                )

            rows.append(project)

        return rows
        

def get_project(project_id: str):

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT
                    id,
                    project_id,
                    project_name,
                    description,
                    status,
                    enable_db,
                    enable_global_kb,
                    service_start_date,
                    service_end_date,
                    subscription_tier,
                    max_queries_per_day,
                    max_storage_mb,
                    created_by,
                    created_at,
                    updated_at,
                    deleted_at,
                    email,
                    role
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

        project = dict(result._mapping)

        docs = conn.execute(
            text(
                """
                SELECT
                    id,
                    document_name,
                    s3_path
                FROM project_documents
                WHERE project_id = :project_db_id
                ORDER BY id
                """
            ),
            {
                "project_db_id": result.id
            }
        ).fetchall()

        project["docPath"] = []

        for doc in docs:

            project["docPath"].append(
                {
                    "docId": doc.id,
                    "docName": doc.document_name,
                    "docpath": doc.s3_path
                }
            )

        return project


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
def update_project_status(
    project_id: str,
    status: str
):

    allowed_status = [
        "active",
        "inactive",
        "maintenance"
    ]

    if status not in allowed_status:

        return {
            "status": "error",
            "message": "Invalid status"
        }

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET status = :status
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id,
                "status": status
            }
        )

        if result.rowcount == 0:

            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": f"Project status updated to {status}"
    }


def update_database_status(
    project_id: str,
    enable_db: bool
):

    with engine.begin() as conn:

        result = conn.execute(
            text(
                """
                UPDATE projects
                SET enable_db = :enable_db
                WHERE project_id = :project_id
                """
            ),
            {
                "project_id": project_id,
                "enable_db": enable_db
            }
        )

        if result.rowcount == 0:

            return {
                "status": "error",
                "message": "Project not found"
            }

    return {
        "status": "success",
        "message": "Database status updated"
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