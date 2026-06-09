from fastapi import APIRouter

from app.services.schema_service import (
    get_database_schema
)

router = APIRouter()


@router.get("/schema")
def schema():

    return get_database_schema()