from __future__ import annotations

from contextlib import nullcontext
import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from backend.app.repositories.contracts.tenant_lifecycle_event_writer_repository import (
    TenantLifecycleEventWriterRepositoryContract,
)


class PostgresTenantLifecycleEventWriterRepository(
    TenantLifecycleEventWriterRepositoryContract
):
    """Canonical PostgreSQL append-only lifecycle event writer.

    The database remains authoritative for:
    - event id generation through the identity column;
    - occurred_at through its server default;
    - event_type whitespace-only rejection;
    - tenant and actor foreign-key integrity;
    - append-only enforcement after insertion.

    When a caller supplies a connection, this repository participates in that
    caller-owned transaction and never commits, rolls back, or closes it.
    Otherwise, the repository owns one transaction through Engine.begin().
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
        if (
            not isinstance(tenant_id, str)
            or not tenant_id.strip()
        ):
            raise ValueError(
                "tenant_id must be non-empty"
            )

        return tenant_id

    @staticmethod
    def _validate_event_type(
        event_type: str,
    ) -> str:
        if not isinstance(event_type, str):
            raise TypeError(
                "event_type must be a string"
            )

        # Preserve the exact caller value.
        # Blank / whitespace-only values are rejected by PostgreSQL.
        return event_type

    @staticmethod
    def _validate_actor_user_id(
        actor_user_id: int | None,
    ) -> int | None:
        if actor_user_id is None:
            return None

        if (
            not isinstance(actor_user_id, int)
            or isinstance(actor_user_id, bool)
        ):
            raise TypeError(
                "actor_user_id must be an integer or None"
            )

        return actor_user_id

    @staticmethod
    def _validate_reason(
        reason: str | None,
    ) -> str | None:
        if reason is None:
            return None

        if not isinstance(reason, str):
            raise TypeError(
                "reason must be a string or None"
            )

        return reason

    @staticmethod
    def _serialize_metadata(
        metadata: dict[str, Any] | None,
    ) -> str | None:
        if metadata is None:
            return None

        if not isinstance(metadata, dict):
            raise TypeError(
                "metadata must be a dict or None"
            )

        return json.dumps(
            metadata,
            ensure_ascii=False,
            separators=(",", ":"),
        )

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
        tenant = self._validate_tenant_id(
            tenant_id
        )
        event = self._validate_event_type(
            event_type
        )
        actor = self._validate_actor_user_id(
            actor_user_id
        )
        reason_value = self._validate_reason(
            reason
        )
        metadata_value = self._serialize_metadata(
            metadata
        )

        statement = text(
            """
            INSERT INTO public.tenant_data_lifecycle_events (
                tenant_id,
                event_type,
                actor_user_id,
                reason,
                metadata
            )
            VALUES (
                :tenant_id,
                :event_type,
                :actor_user_id,
                :reason,
                CAST(:metadata AS JSONB)
            )
            RETURNING
                id,
                tenant_id,
                event_type,
                actor_user_id,
                reason,
                occurred_at,
                metadata
            """
        )

        context = (
            nullcontext(connection)
            if connection is not None
            else self._engine.begin()
        )

        with context as active_connection:
            row = (
                active_connection.execute(
                    statement,
                    {
                        "tenant_id": tenant,
                        "event_type": event,
                        "actor_user_id": actor,
                        "reason": reason_value,
                        "metadata": metadata_value,
                    },
                )
                .mappings()
                .one()
            )

        return dict(row)
