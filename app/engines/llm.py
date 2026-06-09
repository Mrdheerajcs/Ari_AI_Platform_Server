from app.core.llm_provider import LLMProvider

provider = LLMProvider()


def generate_answer(question: str, context: dict):

    answer = provider.generate(
        question,
        context["context"]
    )

    return {
        "question": question,
        "source": context["source"],
        "answer": answer
    }