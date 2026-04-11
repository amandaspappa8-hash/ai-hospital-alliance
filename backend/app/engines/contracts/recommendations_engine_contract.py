from typing import Protocol

class RecommendationsEngineContract(Protocol):
    def __call__(self, medications: list[str], age: int | None) -> dict:
        ...
