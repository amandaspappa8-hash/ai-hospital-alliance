from datetime import datetime
from decimal import Decimal
from uuid import UUID

from backend.app.services.core.tenant_export_service import (
    TenantExportService,
)


class FakeTenantExportRepository:
    FIELD_EXCLUSIONS = {
        "tenants": frozenset({
            "api_key",
        }),
        "users": frozenset({
            "password",
        }),
        "refresh_tokens": frozenset({
            "token_hash",
        }),
    }

    @classmethod
    def export_tables(cls):
        return (
            "refresh_tokens",
            "tenants",
            "users",
        )

    @classmethod
    def excluded_fields_for_table(
        cls,
        table,
    ):
        return cls.FIELD_EXCLUSIONS.get(
            table,
            frozenset(),
        )

    def resolve_scope(
        self,
        *,
        tenant_id,
        principal_user_id,
    ):
        assert tenant_id == "TEN-1"
        assert principal_user_id == 7

        return {
            "tenant_id": "TEN-1",
            "principal_user_id": 7,
            "hospital_id": "H-1",
        }

    def hospital_ids_for_principal(
        self,
        *,
        tenant_id,
        principal_user_id,
    ):
        assert tenant_id == "TEN-1"
        assert principal_user_id == 7

        return [
            "H-2",
            "H-1",
        ]

    def read_tenant_export_rows(
        self,
        *,
        table,
        tenant_id,
        principal_user_id,
    ):
        assert tenant_id == "TEN-1"
        assert principal_user_id == 7

        if table == "tenants":
            return [
                {
                    "id": "TEN-1",
                    "api_key": "SECRET",
                    "name": "Tenant",
                    "amount": Decimal("1.20"),
                }
            ]

        if table == "users":
            return [
                {
                    "id": 7,
                    "password": "SECRET",
                    "hospital_id": "H-1",
                    "created_at":
                    datetime(
                        2026,
                        1,
                        1,
                        12,
                        0,
                        0,
                    ),
                }
            ]

        if table == "refresh_tokens":
            return [
                {
                    "id": 1,
                    "user_id": "7",
                    "token_hash": "SECRET",
                    "marker":
                    UUID(
                        "00000000-0000-0000-0000-000000000001"
                    ),
                }
            ]

        raise AssertionError(table)

    def excluded_tables(self):
        return [
            {
                "table":
                "ahos_28_1_tenants",
                "reason":
                "LEGACY_AHOS28_UNBRIDGED",
            },
            {
                "table":
                "alembic_version",
                "reason":
                "PLATFORM_INTERNAL",
            },
        ]

    def count_unscoped_exclusions(self):
        return {
            "alerts": 3,
            "audit_logs": 2,
        }


def test_snapshot_excludes_credentials_and_is_deterministic():
    service = TenantExportService(
        FakeTenantExportRepository()
    )

    first = (
        service
        .build_tenant_export_snapshot(
            tenant_id="TEN-1",
            principal_user_id=7,
        )
    )

    second = (
        service
        .build_tenant_export_snapshot(
            tenant_id="TEN-1",
            principal_user_id=7,
        )
    )

    assert first == second

    assert first["format_version"] == 1
    assert first["tenant_id"] == "TEN-1"

    assert first["hospital_ids"] == [
        "H-1",
        "H-2",
    ]

    assert first["table_count"] == 3
    assert first["record_count"] == 3

    assert (
        "api_key"
        not in first["tables"]["tenants"][0]
    )

    assert (
        "password"
        not in first["tables"]["users"][0]
    )

    assert (
        "token_hash"
        not in first[
            "tables"
        ]["refresh_tokens"][0]
    )

    assert (
        first[
            "excluded_fields"
        ]["tenants"]
        == ["api_key"]
    )

    assert (
        "unscoped_exclusions"
        not in first
    )


def test_normalization_contract():
    service = TenantExportService(
        FakeTenantExportRepository()
    )

    assert (
        service._normalize_value(
            Decimal("2.500")
        )
        == "2.500"
    )

    assert (
        service._normalize_value(
            UUID(
                "00000000-0000-0000-0000-000000000001"
            )
        )
        == "00000000-0000-0000-0000-000000000001"
    )

    assert (
        service._normalize_value(
            b"\x01\x02"
        )
        == "AQI="
    )


def test_duplicate_canonical_rows_fail_closed():
    service = TenantExportService(
        FakeTenantExportRepository()
    )

    rows = [
        {
            "id": 1,
            "name": "same",
        },
        {
            "name": "same",
            "id": 1,
        },
    ]

    try:
        service._sanitize_rows(
            table="tenants",
            rows=rows,
        )
    except RuntimeError:
        pass
    else:
        raise AssertionError(
            "duplicate canonical rows were accepted"
        )
