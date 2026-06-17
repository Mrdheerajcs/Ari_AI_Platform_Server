from app.services.vector_store import (
    search_global_knowledge
)


def get_global_answer(question: str):

    return search_global_knowledge(
        question
    )