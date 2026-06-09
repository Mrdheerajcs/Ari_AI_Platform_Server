from sentence_transformers import SentenceTransformer
from sentence_transformers import util


class LLMProvider:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate(
        self,
        question: str,
        context: str
    ):

        if not context:
            return "No information found."

        return context