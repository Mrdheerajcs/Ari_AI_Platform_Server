from fastapi import APIRouter

from app.models.project_config import ProjectConfig

from app.services.project_config_service import (
    save_config,
    get_config
)

router = APIRouter()


@router.post("/projects/{project_id}/config")
def configure_project(
    project_id: str,
    config: ProjectConfig
):

    return save_config(
        project_id,
        config.dict()
    )


@router.get("/projects/{project_id}/config")
def get_project_config(
    project_id: str
):

    return get_config(project_id)