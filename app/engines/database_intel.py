from sqlalchemy import text

from app.core.database import engine
from app.services.semantic_table_service import (
    find_best_table
)


def get_database_answer(
    project_id: str,
    question: str
):

    try:

        table_name = find_best_table(
            question
        )

        if not table_name:
            return "No relevant table found."

        with engine.connect() as conn:

            rows = conn.execute(
                text(
                    f"""
                    SELECT *
                    FROM {table_name}
                    LIMIT 5
                    """
                )
            )

            results = []

            for row in rows:

                results.append(
                    str(
                        dict(
                            row._mapping
                        )
                    )
                )

            if not results:
                return (
                    f"No data found in "
                    f"{table_name}"
                )

            return (
                f"Table: {table_name}\n\n"
                + "\n".join(results)
            )

    except Exception as e:

        return (
            f"Database Error: "
            f"{str(e)}"
        )