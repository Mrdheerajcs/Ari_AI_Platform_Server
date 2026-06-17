from sqlalchemy import text
from app.core.database import engine
import bcrypt


def encrypt_password(
    password: str
):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def create_database_config(
    project_id: str,
    db_type: str,
    host: str,
    port: int,
    database_name: str,
    username: str,
    password: str
):

    encrypted_password = encrypt_password(
        password
    )

    with engine.begin() as conn:

        project = conn.execute(
            text("""
                SELECT id
                FROM projects
                WHERE project_id = :project_id
            """),
            {
                "project_id": project_id
            }
        ).fetchone()

        if not project:

            return {
                "status": "error",
                "message": "Project not found"
            }

        conn.execute(
            text("""
                INSERT INTO project_database_config
                (
                    project_id,
                    db_type,
                    host,
                    port,
                    database_name,
                    username,
                    password_encrypted
                )
                VALUES
                (
                    :project_id,
                    :db_type,
                    :host,
                    :port,
                    :database_name,
                    :username,
                    :password
                )
            """),
            {
                "project_id": project.id,
                "db_type": db_type,
                "host": host,
                "port": port,
                "database_name": database_name,
                "username": username,
                "password": encrypted_password
            }
        )

    return {
        "status": "success",
        "message": "Database configuration created"
    }


def get_database_configs(
    project_id: str
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    project_id,
                    db_type,
                    host,
                    port,
                    database_name,
                    username,
                    status
                FROM project_database_config
                WHERE project_id =
                (
                    SELECT id
                    FROM projects
                    WHERE project_id = :project_id
                )
                ORDER BY id
            """),
            {
                "project_id": project_id
            }
        )

        rows = []

        for row in result:

            rows.append(
                dict(row._mapping)
            )

        return rows


def get_database_config(
    config_id: int
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    project_id,
                    db_type,
                    host,
                    port,
                    database_name,
                    username,
                    status
                FROM project_database_config
                WHERE id = :id
            """),
            {
                "id": config_id
            }
        ).fetchone()

        if not result:

            return {
                "status": "error",
                "message": "Config not found"
            }

        return dict(result._mapping)


def update_database_config(
    config_id: int,
    db_type: str,
    host: str,
    port: int,
    database_name: str,
    username: str,
    password: str
):

    encrypted_password = encrypt_password(
        password
    )

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE project_database_config
                SET
                    db_type = :db_type,
                    host = :host,
                    port = :port,
                    database_name = :database_name,
                    username = :username,
                    password_encrypted = :password
                WHERE id = :id
            """),
            {
                "id": config_id,
                "db_type": db_type,
                "host": host,
                "port": port,
                "database_name": database_name,
                "username": username,
                "password": encrypted_password
            }
        )

        if result.rowcount == 0:

            return {
                "status": "error",
                "message": "Config not found"
            }

    return {
        "status": "success",
        "message": "Database configuration updated"
    }


def get_all_database_configs():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    dc.id,
                    p.project_id,
                    p.project_name,
                    dc.db_type,
                    dc.host,
                    dc.port,
                    dc.database_name,
                    dc.username,
                    dc.status
                FROM project_database_config dc
                JOIN projects p
                    ON p.id = dc.project_id
                ORDER BY dc.id
            """)
        )

        rows = []

        for row in result:

            rows.append(
                dict(row._mapping)
            )

        return rows


def update_database_config_status(
    project_id: str,
    config_id: int,
    status: str
):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE project_database_config
                SET status = :status
                WHERE id = :id
                AND project_id =
                (
                    SELECT id
                    FROM projects
                    WHERE project_id = :project_id
                )
            """),
            {
                "project_id": project_id,
                "id": config_id,
                "status": status
            }
        )

        if result.rowcount == 0:

            return {
                "status": "error",
                "message": "Database configuration not found"
            }

    return {
        "status": "success",
        "message": f"Status updated to {status}"
    }

