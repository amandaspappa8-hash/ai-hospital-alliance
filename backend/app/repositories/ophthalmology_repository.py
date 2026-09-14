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

    @abstractmethod
    def list_reports(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_audit_logs(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    def list_cases(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        q: str = "",
    ) -> list[dict[str, Any]]:
        """Return ophthalmology cases in verified tenant/hospital scope."""
        raise NotImplementedError
