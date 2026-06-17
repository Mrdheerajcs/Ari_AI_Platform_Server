from pydantic import BaseModel


class DBConnectionStatusUpdate(BaseModel):
    status: str