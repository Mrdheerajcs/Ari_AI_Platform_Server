from pydantic import BaseModel


class DatabaseStatusUpdate(BaseModel):
    enable_db: bool