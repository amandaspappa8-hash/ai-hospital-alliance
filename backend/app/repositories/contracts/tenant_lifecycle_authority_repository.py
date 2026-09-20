from __future__ import annotations

from typing import Any, Protocol


class TenantLifecycleAuthorityRepositoryContract(
    Protocol
):
    """Read-only lifecycle disposition authority boundary."""

    def get_by_tenant_id(
        self,
        *,
        tenant_id: str,
        connection: Any | None = None,
    ) -> dict[str, Any] | None:
        ...
