from contextlib import contextmanager

import pytest

from backend.app.repositories.postgres.audit_logs_repository import (
    PostgresAuditLogsRepository,
)


class FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def mappings(self):
        return self

    def all(self):
        return list(self._rows)


class FakeConnection:
    def __init__(
        self,
        *,
        principal_rows,
        audit_rows,
    ):
        self.principal_rows = principal_rows
        self.audit_rows = audit_rows
        self.calls = []

    def execute(
        self,
        statement,
        params=None,
    ):
        sql = str(statement)

        self.calls.append(
            (
                sql,
                dict(params or {}),
            )
        )

        if "FROM public.users AS u" in sql:
            return FakeResult(
                self.principal_rows
            )

        if "FROM public.audit_logs AS al" in sql:
            tenant_id = (
                params or {}
            ).get("tenant_id")

            rows = [
                row
                for row in self.audit_rows
                if row.get("tenant_id")
                == tenant_id
            ]

            # Physical SELECT does not return tenant_id.
            projected = [
                {
                    key: value
                    for key, value in row.items()
                    if key != "tenant_id"
                }
                for row in rows
            ]

            return FakeResult(projected)

        raise AssertionError(
            "Unexpected SQL: " + sql
        )


class FakeEngine:
    def __init__(self, connection):
        self.connection = connection

    @contextmanager
    def connect(self):
        yield self.connection


def build_repo(
    *,
    principal_rows=None,
    audit_rows=None,
):
    connection = FakeConnection(
        principal_rows=(
            principal_rows
            if principal_rows is not None
            else [
                {
                    "user_id": 7,
                    "hospital_id": "H-001",
                    "tenant_id": "TENANT-A",
                }
            ]
        ),
        audit_rows=(
            audit_rows
            if audit_rows is not None
            else [
                {
                    "id": 11,
                    "user_id": "doctor1",
                    "action": "read",
                    "resource": "Patient",
                    "success": True,
                    "timestamp": "2026-09-15T10:00:00",
                    "ip_address": "127.0.0.1",
                    "tenant_id": "TENANT-A",
                },
                {
                    "id": 12,
                    "user_id": "doctor2",
                    "action": "read",
                    "resource": "Patient",
                    "success": True,
                    "timestamp": "2026-09-15T10:01:00",
                    "ip_address": "127.0.0.2",
                    "tenant_id": "TENANT-B",
                },
                {
                    "id": 13,
                    "user_id": "legacy",
                    "action": "legacy",
                    "resource": "Legacy",
                    "success": True,
                    "timestamp": "2026-09-15T10:02:00",
                    "ip_address": None,
                    "tenant_id": None,
                },
            ]
        ),
    )

    return (
        PostgresAuditLogsRepository(
            FakeEngine(connection)
        ),
        connection,
    )


def test_scoped_read_returns_only_matching_tenant():
    repository, connection = build_repo()

    rows = repository.list_for_principal(
        tenant_id="TENANT-A",
        principal_user_id=7,
        limit=50,
    )

    assert rows == [
        {
            "id": 11,
            "user_id": "doctor1",
            "action": "read",
            "resource": "Patient",
            "success": True,
            "timestamp": "2026-09-15T10:00:00",
            "ip": "127.0.0.1",
        }
    ]

    audit_sql, params = connection.calls[-1]

    assert (
        "WHERE al.tenant_id = :tenant_id"
        in audit_sql
    )

    assert params["tenant_id"] == "TENANT-A"


def test_null_tenant_rows_are_not_returned():
    repository, _ = build_repo()

    rows = repository.list_for_principal(
        tenant_id="TENANT-A",
        principal_user_id=7,
        limit=50,
    )

    assert all(
        row["user_id"] != "legacy"
        for row in rows
    )


def test_tenant_mismatch_fails_closed():
    repository, _ = build_repo()

    with pytest.raises(
        PermissionError,
        match="does not match",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-B",
            principal_user_id=7,
            limit=50,
        )


@pytest.mark.parametrize(
    "principal",
    [
        None,
        "",
        "abc",
        0,
        -1,
    ],
)
def test_invalid_principal_fails_closed(
    principal,
):
    repository, _ = build_repo()

    with pytest.raises(PermissionError):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=principal,
            limit=50,
        )


def test_unresolved_principal_fails_closed():
    repository, _ = build_repo(
        principal_rows=[],
    )

    with pytest.raises(
        PermissionError,
        match="unresolved",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=999,
            limit=50,
        )


def test_empty_tenant_fails_closed():
    repository, _ = build_repo()

    with pytest.raises(PermissionError):
        repository.list_for_principal(
            tenant_id="",
            principal_user_id=7,
            limit=50,
        )


@pytest.mark.parametrize(
    "limit",
    [
        0,
        -1,
        101,
        "abc",
    ],
)
def test_invalid_limit_rejected(
    limit,
):
    repository, _ = build_repo()

    with pytest.raises(ValueError):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=7,
            limit=limit,
        )


def test_repository_is_read_only():
    repository, connection = build_repo()

    repository.list_for_principal(
        tenant_id="TENANT-A",
        principal_user_id=7,
        limit=50,
    )

    combined_sql = "\n".join(
        sql
        for sql, _ in connection.calls
    ).upper()

    for forbidden in (
        "INSERT ",
        "UPDATE ",
        "DELETE ",
        "ALTER ",
        "DROP ",
        "CREATE ",
    ):
        assert forbidden not in combined_sql
