from typing import Protocol

class DoseSafetyEngineContract(Protocol):
    def __call__(self, medications: list[str], age: int | None) -> dict:
        ...
