from fastapi import HTTPException
from ...security.password_verifier import verify_password
from ...legacy_security import create_access_token


class AuthService:
    def __init__(self, users_repository):
        self.users_repository = users_repository

    def login(self, username: str, password: str) -> dict:
        user = self.users_repository.get_by_username(username)

        if not user or not verify_password(
            password,
            user.get("password", ""),
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        if user.get("is_active") is False:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        tenant_id = user.get("tenant_id")
        identifier = user.get("username")
        role = user.get("role")
        user_id = user.get("id")

        if (
            not tenant_id
            or not identifier
            or role is None
            or user_id is None
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        claims = {
            "sub": str(user_id),
            "email": identifier,
            "role": role,
            "tenant_id": tenant_id,
        }

        access_token = create_access_token(claims)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": identifier,
            "role": role,
            "tenant_id": tenant_id,
        }
