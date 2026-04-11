from typing import Protocol

class InteractionsEngineContract(Protocol):
    def __call__(self, medications: list[str]) -> dict:
        ...
