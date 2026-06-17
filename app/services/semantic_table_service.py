from app.services.schema_service import get_database_schema


def find_best_table(question: str):

    schema = get_database_schema()

    question = question.lower()

    for table_name in schema.keys():

        if table_name.lower() in question:
            return table_name

    tables = list(schema.keys())

    if tables:
        return tables[0]

    return None