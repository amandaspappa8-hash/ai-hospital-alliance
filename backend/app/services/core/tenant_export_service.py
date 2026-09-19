from __future__ import annotations

import base64
import json
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID

from backend.app.repositories.postgres.tenant_export_repository import (
    PostgresTenantExportRepository,
)


class TenantExportService:
    """Build an in-memory, read-only tenant export snapshot.

    This phase deliberately does NOT:
      * create ZIP/TAR/files;
      * expose HTTP routes;
      * write audit/database state;
      * trust a client-supplied tenant identity.
    """

    FORMAT_VERSION = 1

    def __init__(
        self,
        repository: PostgresTenantExportRepository,
    ):
        self.repository = repository

    @classmethod
    def _normalize_value(
        cls,
        value: Any,
    ) -> Any:

        if value is None:
            return None

        if isinstance(
            value,
            datetime,
        ):
            if value.tzinfo is None:
                value = value.replace(
                    tzinfo=timezone.utc
                )
            else:
                value = value.astimezone(
                    timezone.utc
                )

            return (
                value
                .isoformat(
                    timespec="microseconds"
                )
                .replace(
                    "+00:00",
                    "Z",
                )
            )

        if isinstance(
            value,
            date,
        ):
            return value.isoformat()

        if isinstance(
            value,
            Decimal,
        ):
            return str(value)

        if isinstance(
            value,
            UUID,
        ):
            return str(value)

        if isinstance(
            value,
            bytes,
        ):
            return base64.b64encode(
                value
            ).decode("ascii")

        if isinstance(
            value,
            dict,
        ):
            return {
                str(key): cls._normalize_value(
                    item
                )
                for key, item in sorted(
                    value.items(),
                    key=lambda pair:
                    str(pair[0]),
                )
            }

        if isinstance(
            value,
            (list, tuple),
        ):
            return [
                cls._normalize_value(
                    item
                )
                for item in value
            ]

        return value

    @classmethod
    def _canonical_json(
        cls,
        value: Any,
    ) -> str:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def _sanitize_rows(
        self,
        *,
        table: str,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        excluded = (
            self.repository
            .excluded_fields_for_table(
                table
            )
        )

        normalized_rows = []

        for row in rows:

            clean = {
                key: self._normalize_value(
                    value
                )
                for key, value
                in row.items()
                if key not in excluded
            }

            clean = dict(
                sorted(
                    clean.items()
                )
            )

            normalized_rows.append(
                clean
            )

        normalized_rows.sort(
            key=self._canonical_json
        )

        serialized = [
            self._canonical_json(
                row
            )
            for row in normalized_rows
        ]

        if len(serialized) != len(
            set(serialized)
        ):
            raise RuntimeError(
                f"Duplicate canonical export rows detected: {table}"
            )

        return normalized_rows

    def _build_snapshot_payload(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
        connection: Any | None = None,
    ) -> dict[str, Any]:

        if connection is None:

            scope = self.repository.resolve_scope(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

            hospital_ids = (
                self.repository
                .hospital_ids_for_principal(
                    tenant_id=scope[
                        "tenant_id"
                    ],
                    principal_user_id=scope[
                        "principal_user_id"
                    ],
                )
            )

        else:

            scope = self.repository.resolve_scope(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
                connection=connection,
            )

            hospital_ids = (
                self.repository
                .hospital_ids_for_principal(
                    tenant_id=scope[
                        "tenant_id"
                    ],
                    principal_user_id=scope[
                        "principal_user_id"
                    ],
                    connection=connection,
                )
            )

        tables: dict[
            str,
            list[dict[str, Any]],
        ] = {}

        record_count = 0

        for table in (
            self.repository.export_tables()
        ):

            if connection is None:

                raw_rows = (
                    self.repository
                    .read_tenant_export_rows(
                        table=table,
                        tenant_id=scope[
                            "tenant_id"
                        ],
                        principal_user_id=scope[
                            "principal_user_id"
                        ],
                    )
                )

            else:

                raw_rows = (
                    self.repository
                    .read_tenant_export_rows(
                        table=table,
                        tenant_id=scope[
                            "tenant_id"
                        ],
                        principal_user_id=scope[
                            "principal_user_id"
                        ],
                        connection=connection,
                    )
                )

            rows = self._sanitize_rows(
                table=table,
                rows=raw_rows,
            )

            tables[table] = rows
            record_count += len(rows)

        excluded_fields = {
            table: sorted(fields)
            for table, fields
            in sorted(
                self.repository
                .FIELD_EXCLUSIONS
                .items()
            )
        }

        if connection is None:

            excluded_tables = (
                self.repository.excluded_tables()
            )

        else:

            excluded_tables = (
                self.repository.excluded_tables(
                    connection=connection,
                )
            )

        return {
            "format_version":
            self.FORMAT_VERSION,
            "tenant_id":
            scope["tenant_id"],
            "hospital_ids":
            sorted(hospital_ids),
            "table_count":
            len(tables),
            "record_count":
            record_count,
            "tables":
            dict(
                sorted(
                    tables.items()
                )
            ),
            "excluded_tables":
            excluded_tables,
            "excluded_fields":
            excluded_fields,
        }

    def build_tenant_export_snapshot(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]:

        engine = getattr(
            self.repository,
            "engine",
            None,
        )

        # Preserve the existing repository protocol for test doubles
        # and alternate in-memory implementations that do not own a
        # PostgreSQL engine.
        if engine is None:

            return self._build_snapshot_payload(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
                connection=None,
            )

        # Canonical PostgreSQL tenant exports are read from exactly one
        # read-only REPEATABLE READ transaction.
        with (
            engine.connect()
            .execution_options(
                isolation_level="REPEATABLE READ"
            )
        ) as connection:

            with connection.begin():

                connection.exec_driver_sql(
                    "SET TRANSACTION READ ONLY"
                )

                return self._build_snapshot_payload(
                    tenant_id=tenant_id,
                    principal_user_id=principal_user_id,
                    connection=connection,
                )
