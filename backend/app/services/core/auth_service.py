from fastapi import HTTPException


class AuthService:
    def __init__(self, users_repository):
        self.users_repository = users_repository

    def login(self, username: str, password: str):
        user = self.users_repository.get_by_username(username)
        if not user or user.get("password") != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": user["token"],
            "token_type": "bearer",
            "user": {
                "username": username,
                "name": user["name"],
                "role": user["role"],
            },
        }
