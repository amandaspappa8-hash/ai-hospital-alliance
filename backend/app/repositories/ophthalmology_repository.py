from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class OphthalmologyRepository(ABC):
    """Canonical Ophthalmology persistence boundary."""

    @abstractmethod
    def list_analyses(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        """Return analyses in verified tenant/hospital scope."""
        raise NotImplementedError
