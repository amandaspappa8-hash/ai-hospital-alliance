from __future__ import annotations

from typing import Any, Protocol


class TenantLifecycleMutationRepositoryContract(Protocol):
    """Canonical tenant lifecycle mutation boundary."""

    def create_initial_lifecycle(
        self,
        *,
        tenant_id: str,
        lifecycle_state: str,
        connection: Any,
    ) -> dict[str, Any]:
        ...
