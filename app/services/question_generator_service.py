import spacy

from app.services.vector_store import (
    get_project_collection
)

# Load once
nlp = spacy.load(
    "en_core_web_sm"
)


def generate_suggested_questions(
    project_id: str
):

    collection = get_project_collection(
        project_id
    )

    results = collection.get()

    documents = results.get(
        "documents",
        []
    )

    if not documents:
        return []

    full_text = "\n".join(
        documents
    )

    doc = nlp(full_text)

    topics = set()

    # Extract noun phrases
    for chunk in doc.noun_chunks:

        topic = chunk.text.strip()

        if len(topic) < 4:
            continue

        if len(topic) > 60:
            continue

        topics.add(topic)

    # Extract named entities
    for ent in doc.ents:

        if ent.label_ in [
            "ORG",
            "PRODUCT",
            "PERSON",
            "GPE",
            "EVENT",
            "WORK_OF_ART"
        ]:

            topics.add(
                ent.text.strip()
            )

    questions = []

    for topic in sorted(topics):

        questions.append(
            f"What is {topic}?"
        )

    # Limit response
    return questions[:25]