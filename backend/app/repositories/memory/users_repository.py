from typing import Any

class InMemoryUsersRepository:
    def __init__(self, users_store: dict[str, Any]):
        self.users_store = users_store

    def get_by_username(self, username: str) -> dict[str, Any] | None:
        user = self.users_store.get(username)
        return user if isinstance(user, dict) else None
