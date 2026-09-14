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

    def get_case_detail(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        case_id: str,
    ) -> dict[str, Any] | None:
        """Return one case with scoped reports and audit logs."""
        raise NotImplementedError

    def get_analysis(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        analysis_id: str,
    ) -> dict[str, Any] | None:
        """Return one analysis in verified tenant/hospital scope."""
        raise NotImplementedError

    def get_annotation(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        annotation_id: str,
    ) -> dict[str, Any] | None:
        """Return one annotation in verified tenant/hospital scope."""
        raise NotImplementedError

    def get_review(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        review_id: str,
    ) -> dict[str, Any] | None:
        """Return one clinical review in verified tenant/hospital scope."""
        raise NotImplementedError
