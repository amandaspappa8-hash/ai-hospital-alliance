from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class AHOSPlugin:
    name: str
    version: str
    category: str
    register: Callable
    description: Optional[str] = None
