from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    email: str
    enable_db: bool