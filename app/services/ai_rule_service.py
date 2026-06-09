AI_RULES = {
    
    "tender": "database",
    "tenders": "database",
    "vendor": "database",
    "vendors": "database",

    "policy": "pdf",
    "invoice": "pdf",
    "gst": "pdf",

    "ari ai": "global",
    "secure": "global"
}
def get_route(question: str):

    question = question.lower()

    for keyword, route in AI_RULES.items():
        if keyword in question:
            return route

    return "database"