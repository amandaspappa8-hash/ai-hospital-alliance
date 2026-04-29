from typing import Any


class InMemoryReportsRepository:
    def __init__(self, reports_store: list[dict[str, Any]]):
        self.reports_store = reports_store

    def list_all(self) -> list[dict[str, Any]]:
        return list(self.reports_store)
