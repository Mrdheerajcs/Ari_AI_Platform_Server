from fastapi import APIRouter, Depends

from app.core.security import authenticate_api

from app.models.project import ProjectCreate
from app.models.project_status import ProjectStatusUpdate
from app.models.database_status import DatabaseStatusUpdate

from app.services.project_registry_service import (
    create_project,
    get_projects,
    get_project,
    update_project,
    update_project_status,
    update_database_status,
    delete_project
)

router = APIRouter()


@router.post("/projects")
def register_project(
    project: ProjectCreate,
    user=Depends(authenticate_api)
):

    return create_project(
        project.name,
        project.description,
        project.email,
        project.enable_db
    )


@router.get("/projects")
def list_projects(
    user=Depends(authenticate_api)
):

    return get_projects()


@router.get("/projects/{project_id}")
def get_project_by_id(
    project_id: str,
    user=Depends(authenticate_api)
):

    return get_project(project_id)


@router.put("/projects/{project_id}")
def update_project_by_id(
    project_id: str,
    project: ProjectCreate,
    user=Depends(authenticate_api)
):

    return update_project(
        project_id,
        project.name,
        project.description,
        project.email,
        project.enable_db
    )


@router.put("/projects/{project_id}/status")
def update_status(
    project_id: str,
    request: ProjectStatusUpdate,
    user=Depends(authenticate_api)
):

    return update_project_status(
        project_id,
        request.status
    )


@router.put("/projects/{project_id}/database")
def update_database(
    project_id: str,
    request: DatabaseStatusUpdate,
    user=Depends(authenticate_api)
):

    return update_database_status(
        project_id,
        request.enable_db
    )


@router.delete("/projects/{project_id}")
def delete_project_by_id(
    project_id: str,
    user=Depends(authenticate_api)
):

    return delete_project(project_id)