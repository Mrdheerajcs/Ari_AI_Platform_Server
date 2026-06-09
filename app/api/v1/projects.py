from fastapi import APIRouter

from app.models.project import ProjectCreate

from app.services.project_registry_service import (
    create_project,
    get_projects
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