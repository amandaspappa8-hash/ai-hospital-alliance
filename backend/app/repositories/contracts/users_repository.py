from typing import Protocol, Any


class UsersRepositoryContract(Protocol):
    def get_by_username(self, username: str) -> dict[str, Any] | None: ...
