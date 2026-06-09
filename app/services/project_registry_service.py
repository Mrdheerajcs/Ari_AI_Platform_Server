from datetime import datetime
from sqlalchemy import text
from app.core.database import engine

PROJECTS = {}


def create_project(
    name: str,
    description: str,
    email: str,
    enable_db: bool
):

    year = datetime.now().strftime("%y")

    project_ids = [
        project_id
        for project_id in PROJECTS.keys()
        if project_id.startswith(
            f"ARI{year}-"
        )
    ]

    if not project_ids:

        next_number = 1

    else:

        max_number = max(
            int(
                project_id.split("-")[1]
            )
            for project_id in project_ids
        )

        next_number = max_number + 1

    project_id = (
        f"ARI{year}-{next_number:03}"
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
                    role
                )
                VALUES
                (
                    :project_id,
                    :project_name,
                    :description,
                    'active',
                    :enable_db,
                    :email,
                    'user'
                )
                """
            ),
            {
                "project_id": project_id,
                "project_name": name,
                "description": description,
                "enable_db": enable_db,
                "email": email
            }
        )

    return {
        "project_id": project_id,
        "name": name,
        "description": description,
        "email": email,
        "role": "user",
        "enable_db": enable_db,
        "active": True
    }


def get_projects():

    return list(
        PROJECTS.values()
    )