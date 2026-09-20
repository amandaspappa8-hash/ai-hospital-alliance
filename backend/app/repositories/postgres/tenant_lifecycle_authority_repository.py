from __future__ import annotations

from contextlib import nullcontext
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from backend.app.repositories.contracts.tenant_lifecycle_authority_repository import (
    TenantLifecycleAuthorityRepositoryContract,
)


class PostgresTenantLifecycleAuthorityRepository(
    TenantLifecycleAuthorityRepositoryContract
):
    """Read-only authority adapter for tenant lifecycle disposition state.

    public.tenant_data_lifecycle is the sole lifecycle disposition
    authority consumed by this repository.

    This adapter does not:
      - infer authority from tenants.is_active;
      - infer authority from tenants.is_verified;
      - initialize lifecycle state;
      - write lifecycle state or events;
      - execute destructive SQL.
    """

    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self._engine = engine

    @property
    def engine(self) -> Engine:
        return self._engine

    @staticmethod
    def _validate_tenant_id(
        tenant_id: str,
    ) -> str:
        value = str(
            tenant_id or ""
        ).strip()

        if not value:
            raise ValueError(
                "tenant_id must be non-empty"
            )

        return value

    def get_by_tenant_id(
        self,
        *,
        tenant_id: str,
        connection: Any | None = None,
    ) -> dict[str, Any] | None:
        tenant = self._validate_tenant_id(
            tenant_id
        )

        statement = text(
            """
            SELECT
                l.tenant_id,
                l.lifecycle_state,
                l.legal_hold_active,
                l.legal_hold_reason,
                l.legal_hold_set_at,
                l.legal_hold_released_at,
                l.retention_until,
                l.offboarding_requested_at,
                l.offboarding_approved_at,
                l.archive_completed_at,
                l.purge_eligible_at,
                l.created_at,
                l.updated_at
            FROM public.tenant_data_lifecycle AS l
            WHERE l.tenant_id = :tenant_id
            """
        )

        context = (
            nullcontext(connection)
            if connection is not None
            else self._engine.connect()
        )

        with context as active_connection:
            rows = (
                active_connection.execute(
                    statement,
                    {
                        "tenant_id": tenant,
                    },
                )
                .mappings()
                .all()
            )

        if not rows:
            return None

        if len(rows) != 1:
            raise RuntimeError(
                "Lifecycle authority is not unique "
                f"for tenant: {tenant}"
            )

        return dict(rows[0])
