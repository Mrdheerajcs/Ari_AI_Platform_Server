import os
import chromadb

BASE_VECTOR_PATH = "data/projects"

os.makedirs(
    BASE_VECTOR_PATH,
    exist_ok=True
)


def get_project_collection(project_id: str):

    project_path = os.path.join(
        BASE_VECTOR_PATH,
        f"proj_{project_id}"
    )

    os.makedirs(
        project_path,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=project_path
    )

    return client.get_or_create_collection(
        name=f"project_{project_id}"
    )


def get_global_collection():

    global_path = os.path.join(
        BASE_VECTOR_PATH,
        "global"
    )

    os.makedirs(
        global_path,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=global_path
    )

    return client.get_or_create_collection(
        name="global_knowledge"
    )


def save_chunks(
    project_id: str,
    document_name: str,
    chunks: list
):

    collection = get_project_collection(
        project_id
    )

    for index, chunk in enumerate(chunks):

        collection.add(
            ids=[
                f"{document_name}_{index}"
            ],
            documents=[
                chunk
            ],
            metadatas=[
                {
                    "source_file": document_name,
                    "chunk_index": index,
                    "total_chunks": len(chunks),
                    "project_id": project_id
                }
            ]
        )

    return True


def save_global_chunks(
    document_name: str,
    chunks: list
):

    collection = get_global_collection()

    for index, chunk in enumerate(chunks):

        collection.add(
            ids=[
                f"{document_name}_{index}"
            ],
            documents=[
                chunk
            ],
            metadatas=[
                {
                    "source_file": document_name,
                    "chunk_index": index,
                    "total_chunks": len(chunks)
                }
            ]
        )

    return True


def search_project_knowledge(
    project_id: str,
    question: str
):

    collection = get_project_collection(
        project_id
    )

    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    if not results["documents"]:
        return None

    return "\n\n".join(
        results["documents"][0]
    )


def search_global_knowledge(
    question: str
):

    collection = get_global_collection()

    results = collection.query(
        query_texts=[question],
        n_results=1
    )

    if not results["documents"]:
        return None

    return results["documents"][0][0]