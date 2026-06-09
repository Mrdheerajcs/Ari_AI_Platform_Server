from sqlalchemy import text

from app.core.database import engine


def get_database_schema():

    schema = {}

    with engine.connect() as conn:

        tables = conn.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
            """)
        )

        for table in tables:

            table_name = table[0]

            columns = conn.execute(
                text(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='{table_name}'
                """)
            )

            schema[table_name] = [
                column[0]
                for column in columns
            ]

    return schema