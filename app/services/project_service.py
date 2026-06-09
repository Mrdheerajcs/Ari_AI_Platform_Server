from sqlalchemy import text

from app.core.database import engine


def validate_project(project_id: str):

    try:

        with engine.connect() as conn:

            result = conn.execute(
                text(
                    """
                    SELECT project_id,
                           status
                    FROM projects
                    WHERE project_id = :project_id
                    """
                ),
                {
                    "project_id": project_id
                }
            ).fetchone()

            print("PROJECT ID RECEIVED:", project_id)
            print("DATABASE RESULT:", result)

            if not result:
                return False

            return True

    except Exception as e:

        print("PROJECT VALIDATION ERROR:", e)

        return False