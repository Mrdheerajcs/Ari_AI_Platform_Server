RULES = {
    "viewer": {
        "database": False,
        "pdf": True,
        "global": True
    },
    "manager": {
        "database": True,
        "pdf": True,
        "global": True
    },
    "admin": {
        "database": True,
        "pdf": True,
        "global": True
    }
}


def is_source_allowed(role: str, source: str):

    role_rules = RULES.get(role.lower())

    if not role_rules:
        return False

    return role_rules.get(source, False)