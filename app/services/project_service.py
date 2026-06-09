from app.services.project_registry_service import PROJECTS


def validate_project(project_id: str):

    print("PROJECT ID RECEIVED:", project_id)
    print("ALL PROJECTS:", PROJECTS)

    project = PROJECTS.get(project_id)

    if not project:
        return False

    return project.get("active", False)