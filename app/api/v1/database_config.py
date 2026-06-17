from fastapi import APIRouter, Depends

from app.core.security import authenticate_api

from app.models.db_connection import (
    DBConnectionCreate,
    DBConnectionUpdate
)

from app.models.db_connection_status import (
    DBConnectionStatusUpdate
)

from app.services.database_config_service import (
    create_database_config,
    get_database_configs,
    get_database_config,
    update_database_config,
    get_all_database_configs,
    update_database_config_status
)

router = APIRouter()


@router.post("/projects/{project_id}/database-config")
def create_config(
    project_id: str,
    request: DBConnectionCreate,
    user=Depends(authenticate_api)
):

    return create_database_config(
        project_id=project_id,
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        database_name=request.database_name,
        username=request.username,
        password=request.password
    )


@router.get("/projects/{project_id}/database-config")
def get_configs(
    project_id: str,
    user=Depends(authenticate_api)
):

    return get_database_configs(
        project_id
    )


@router.get(
    "/projects/{project_id}/database-config/{config_id}"
)
def get_config(
    project_id: str,
    config_id: int,
    user=Depends(authenticate_api)
):

    return get_database_config(
        config_id
    )


@router.put(
    "/projects/{project_id}/database-config/{config_id}"
)
def update_config(
    project_id: str,
    config_id: int,
    request: DBConnectionUpdate,
    user=Depends(authenticate_api)
):

    return update_database_config(
        config_id=config_id,
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        database_name=request.database_name,
        username=request.username,
        password=request.password
    )


@router.get("/database-config")
def get_all_configs(
    user=Depends(authenticate_api)
):

    return get_all_database_configs()


@router.put("/database-config/{config_id}/status")
def update_status(
    config_id: int,
    request: DBConnectionStatusUpdate,
    user=Depends(authenticate_api)
):

    return update_database_config_status(
        config_id,
        request.status
    )