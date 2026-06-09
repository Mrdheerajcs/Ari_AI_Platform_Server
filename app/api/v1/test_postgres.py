from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine

router = APIRouter()


@router.get("/postgres-test")
def postgres_test():

    try:

        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW()"))

            return {
                "status": "success",
                "result": str(result.fetchone()[0])
            }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/tables")
def get_tables():

    try:

        with engine.connect() as conn:

            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))

            return {
                "status": "success",
                "tables": [row[0] for row in result]
            }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
@router.get("/columns/{table_name}")
def get_columns(table_name: str):

    try:

        with engine.connect() as conn:

            result = conn.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
            """))

            return {
                "status": "success",
                "table": table_name,
                "columns": [row[0] for row in result]
            }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
@router.get("/tenders")
def get_tenders():

    try:

        with engine.connect() as conn:

            result = conn.execute(text("""
                SELECT
                    tender_no,
                    tender_title,
                    project_name,
                    estimated_value,
                    tender_status
                FROM publish_tender_header
                LIMIT 10
            """))

            data = []

            for row in result:
                data.append({
                    "tender_no": row[0],
                    "tender_title": row[1],
                    "project_name": row[2],
                    "estimated_value": str(row[3]),
                    "tender_status": row[4]
                })

            return {
                "status": "success",
                "data": data
            }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
@router.get("/columns/{table_name}")
def get_columns(table_name: str):

    with engine.connect() as conn:

        result = conn.execute(text(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
        """))

        return {
            "table": table_name,
            "columns": [row[0] for row in result]
        }