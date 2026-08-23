from dataclasses import dataclass
from typing import Optional


@dataclass
class AHOSService:
    name: str
    version: str
    category: str
    status: str
    endpoint: str
    description: Optional[str] = None
