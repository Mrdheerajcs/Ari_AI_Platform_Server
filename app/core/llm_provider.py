class LLMProvider:

    def __init__(self):
        pass

    def generate(
        self,
        question: str,
        context: str
    ):

        if not context:
            return "No information found."

        sentences = context.split(".")

        question_words = question.lower().split()

        for sentence in sentences:

            for word in question_words:

                if word in sentence.lower():
                    return sentence.strip()

        return context[:300]