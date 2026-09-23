from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from backend.app.repositories.contracts.tenant_lifecycle_mutation_repository import (
    TenantLifecycleMutationRepositoryContract,
)


class PostgresTenantLifecycleMutationRepository(
    TenantLifecycleMutationRepositoryContract
):
    """Caller-owned transaction lifecycle initialization repository."""

    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self._engine = engine

    @property
    def engine(self) -> Engine:
        return self._engine

    @staticmethod
    def _nonblank(
        name: str,
        value: str,
    ) -> str:
        if (
            not isinstance(value, str)
            or not value.strip()
        ):
            raise ValueError(
                f"{name} must be a non-empty string"
            )

        return value

    def create_initial_lifecycle(
        self,
        *,
        tenant_id: str,
        lifecycle_state: str,
        connection: Any,
    ) -> dict[str, Any]:
        tenant = self._nonblank(
            "tenant_id",
            tenant_id,
        )

        state = self._nonblank(
            "lifecycle_state",
            lifecycle_state,
        )

        row = (
            connection.execute(
                text(
                    """
                    INSERT INTO public.tenant_data_lifecycle (
                        tenant_id,
                        lifecycle_state,
                        legal_hold_active,
                        legal_hold_reason,
                        legal_hold_set_at,
                        legal_hold_released_at,
                        retention_until,
                        offboarding_requested_at,
                        offboarding_approved_at,
                        archive_completed_at,
                        purge_eligible_at
                    )
                    VALUES (
                        :tenant_id,
                        :lifecycle_state,
                        FALSE,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL,
                        NULL
                    )
                    RETURNING
                        tenant_id,
                        lifecycle_state,
                        legal_hold_active,
                        legal_hold_reason,
                        legal_hold_set_at,
                        legal_hold_released_at,
                        retention_until,
                        offboarding_requested_at,
                        offboarding_approved_at,
                        archive_completed_at,
                        purge_eligible_at,
                        created_at,
                        updated_at
                    """
                ),
                {
                    "tenant_id": tenant,
                    "lifecycle_state": state,
                },
            )
            .mappings()
            .one()
        )

        return dict(row)
