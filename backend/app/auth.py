from .security import hash_password, verify_password, create_access_token


def create_token(data: dict) -> str:
    return create_access_token(data)


from .security_jwt import get_current_user
