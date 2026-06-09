from pydantic import BaseModel

class ChatRequest(BaseModel):
    project_id: str
    user_id: str
    role: str
    question: str