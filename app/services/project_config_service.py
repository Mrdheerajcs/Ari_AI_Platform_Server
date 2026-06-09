PROJECT_CONFIGS = {
    "ARI26-001": {
        "allowed_tables": [
            "publish_tender_header"
        ],
        "hidden_fields": [],
        "allowed_sources": [
            "database",
            "pdf",
            "global"
        ]
    }
}


def save_config(project_id: str, config: dict):

    PROJECT_CONFIGS[project_id] = config

    return PROJECT_CONFIGS[project_id]


def get_config(project_id: str):

    return PROJECT_CONFIGS.get(
        project_id,
        {
            "allowed_tables": [],
            "hidden_fields": [],
            "allowed_sources": [
                "database",
                "pdf",
                "global"
            ]
        }
    )