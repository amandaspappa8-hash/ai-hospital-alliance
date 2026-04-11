from typing import Protocol

class DischargeCounselingEngineContract(Protocol):
    def __call__(self, medications: list[str]) -> dict:
        ...
