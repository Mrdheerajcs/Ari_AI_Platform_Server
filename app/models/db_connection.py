from pydantic import BaseModel


class DBConnectionCreate(BaseModel):
    db_type: str
    host: str
    port: int
    database_name: str
    username: str
    password: str


class DBConnectionUpdate(BaseModel):
    db_type: str
    host: str
    port: int
    database_name: str
    username: str
    password: str