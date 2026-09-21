from __future__ import annotations

from typing import Any, Protocol


class TenantLifecycleEventWriterRepositoryContract(Protocol):
    """Canonical append-only tenant lifecycle event writer boundary."""

    def append_event(
        self,
        *,
        tenant_id: str,
        event_type: str,
        actor_user_id: int | None = None,
        reason: str | None = None,
        metadata: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> dict[str, Any]:
        """Append one immutable lifecycle event and return its persisted row."""
        ...
