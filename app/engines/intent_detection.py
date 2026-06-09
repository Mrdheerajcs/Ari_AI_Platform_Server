from app.services.ai_rule_service import get_route


def detect_intent(question: str):
    return get_route(question)