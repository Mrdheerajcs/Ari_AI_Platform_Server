from app.services.vector_store import (
    search_project_knowledge
)


def search_documents(
    project_id: str,
    question: str
):

    result = search_project_knowledge(
        project_id=project_id,
        question=question
    )

    if not result:
        return None

    return result
