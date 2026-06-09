from sqlalchemy import text
from app.core.database import engine


def get_latest_tenders():

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT
                tender_no,
                tender_title,
                estimated_value,
                tender_status
            FROM publish_tender_header
            LIMIT 5
        """))

        tenders = []

        for row in result:
            tenders.append(
                f"{row[0]} | {row[1]} | ₹{row[2]} | {row[3]}"
            )

        return "\n".join(tenders)