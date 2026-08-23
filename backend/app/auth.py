from .security_compat import hash_password, verify_password, issue_access_token


def create_token(data: dict) -> str:
    return issue_access_token(data)


from .security_compat import get_current_user
