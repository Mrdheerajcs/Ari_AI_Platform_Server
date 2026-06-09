ALLOWED_ROLES = [
    "admin",
    "manager",
    "viewer"
]


def validate_role(role: str):
    return role.lower() in ALLOWED_ROLES