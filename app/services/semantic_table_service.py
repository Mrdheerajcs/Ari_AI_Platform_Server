from sentence_transformers import SentenceTransformer
from sentence_transformers import util

from app.services.schema_service import get_database_schema

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

schema = get_database_schema()

table_embeddings = {}

for table_name, columns in schema.items():

    table_text = (
        table_name
        + " "
        + " ".join(columns)
    )

    table_embeddings[table_name] = model.encode(
        table_text,
        convert_to_tensor=True
    )


def find_best_table(question: str):

    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    best_table = None
    best_score = 0

    for table_name, embedding in table_embeddings.items():

        score = util.cos_sim(
            question_embedding,
            embedding
        ).item()

        if score > best_score:
            best_score = score
            best_table = table_name

    return best_table