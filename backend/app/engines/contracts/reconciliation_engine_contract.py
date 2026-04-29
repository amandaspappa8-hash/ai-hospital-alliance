from typing import Protocol


class ReconciliationEngineContract(Protocol):
    def __call__(self, medications: list[str]) -> dict: ...
