GLOBAL_KB = {
    "what is ari ai?": "ARI AI is a centralized enterprise AI platform.",
    "how does ari ai work?": "ARI AI processes your questions and routes them through the appropriate engines.",
    "is my data secure?": "Yes, ARI AI provides complete project isolation and secure access."
}

def get_global_answer(question: str):
    return GLOBAL_KB.get(question.lower())