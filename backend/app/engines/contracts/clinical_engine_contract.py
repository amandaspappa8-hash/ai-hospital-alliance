from typing import Protocol, Any

class ClinicalRoutingEngineContract(Protocol):
    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...
