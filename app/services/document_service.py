from app.api.v1.documents import DOCUMENTS


def search_documents(project_id: str, question: str):

    question = question.lower()

    documents = DOCUMENTS.get(project_id, [])

    for doc in documents:

        if "chunks" in doc:

            for chunk in doc["chunks"]:

                chunk_lower = chunk.lower()

                if any(word in chunk_lower for word in question.split()):
                    return chunk

        elif "text" in doc:

            text = doc["text"].lower()

            if any(word in text for word in question.split()):
                return doc["text"]

    return None