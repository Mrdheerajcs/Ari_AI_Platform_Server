CHAT_HISTORY = []

def save_chat(user_id, question, answer):

    CHAT_HISTORY.append({
        "user_id": user_id,
        "question": question,
        "answer": answer
    })

def get_history():
    return CHAT_HISTORY