from fastapi import APIRouter

from app.models.project import ProjectCreate

from app.services.project_registry_service import (
    create_project,
    get_projects,
    get_project,
    update_project,
    activate_project,
    deactivate_project,
    maintenance_project,
    delete_project
)
router = APIRouter()


@router.post("/projects")
def register_project(project: ProjectCreate):

    return create_project(
        project.name,
        project.description,
        project.email,
        project.enable_db
    )


@router.get("/projects")
def list_projects():

    return get_projects()


@router.get("/projects/{project_id}")
def get_project_by_id(project_id: str):

    return get_project(project_id)


@router.put("/projects/{project_id}")
def update_project_by_id(
    project_id: str,
    project: ProjectCreate
):

    return update_project(
        project_id,
        project.name,
        project.description,
        project.email,
        project.enable_db
    )
@router.post("/projects/{project_id}/activate")
def activate_project_by_id(project_id: str):

    return activate_project(project_id)


@router.post("/projects/{project_id}/deactivate")
def deactivate_project_by_id(project_id: str):

    return deactivate_project(project_id)


@router.put("/projects/{project_id}/maintenance")
def maintenance_project_by_id(project_id: str):

    return maintenance_project(project_id)


@router.delete("/projects/{project_id}")
def delete_project_by_id(project_id: str):

    return delete_project(project_id)