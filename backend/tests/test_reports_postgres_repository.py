from __future__ import annotations

import pytest

from backend.app.repositories.postgres.reports_repository import (
    PostgresReportsRepository,
)


class FakeMappingsResult:
    def __init__(
        self,
        *,
        one=None,
        rows=None,
    ):
        self._one = one
        self._rows = rows or []

    def one_or_none(self):
        return self._one

    def all(self):
        return list(
            self._rows
        )


class FakeExecuteResult:
    def __init__(
        self,
        *,
        one=None,
        rows=None,
    ):
        self._one = one
        self._rows = rows or []

    def mappings(self):
        return FakeMappingsResult(
            one=self._one,
            rows=self._rows,
        )


class FakeConnection:
    def __init__(
        self,
        engine,
    ):
        self.engine = engine

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        return False

    def execute(
        self,
        statement,
        params,
    ):
        sql = str(
            statement
        )

        self.engine.calls.append(
            {
                "sql": sql,
                "params": dict(params),
            }
        )

        if "FROM public.users AS u" in sql:
            return FakeExecuteResult(
                one=self.engine.principal_row
            )

        if "FROM public.reports AS r" in sql:
            return FakeExecuteResult(
                rows=self.engine.report_rows
            )

        raise AssertionError(
            "Unexpected SQL: "
            + sql
        )


class FakeEngine:
    def __init__(
        self,
        *,
        principal_row=None,
        report_rows=None,
    ):
        self.principal_row = (
            principal_row
        )

        self.report_rows = (
            report_rows
            or []
        )

        self.calls = []

    def connect(self):
        return FakeConnection(
            self
        )


def test_list_for_principal_returns_canonical_contract():
    engine = FakeEngine(
        principal_row={
            "tenant_id":
                "TENANT-A",
        },
        report_rows=[
            {
                "id": "R-1001",
                "patient_id":
                    "P-1001",
                "title":
                    "Clinical Report",
                "type":
                    "Clinical",
                "status":
                    "Ready",
                "body":
                    "Body text",
            }
        ],
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    rows = (
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=7,
        )
    )

    assert rows == [
        {
            "id": "R-1001",
            "patient_id": "P-1001",
            "title": "Clinical Report",
            "type": "Clinical",
            "status": "Ready",
            "body": "Body text",
        }
    ]

    assert len(
        engine.calls
    ) == 2

    scope_sql = (
        engine.calls[0]["sql"]
    )

    reports_sql = (
        engine.calls[1]["sql"]
    )

    assert (
        "FROM public.users AS u"
        in scope_sql
    )

    assert (
        "JOIN public.hospitals AS h"
        in scope_sql
    )

    assert (
        "JOIN public.tenants AS t"
        in scope_sql
    )

    assert (
        "u.is_active IS TRUE"
        in scope_sql
    )

    assert (
        "FROM public.reports AS r"
        in reports_sql
    )

    assert (
        "JOIN public.patients AS p"
        in reports_sql
    )

    assert (
        "JOIN public.hospitals AS h"
        in reports_sql
    )

    assert (
        "WHERE h.tenant_id = :tenant_id"
        in reports_sql
    )

    assert engine.calls[1][
        "params"
    ] == {
        "tenant_id":
            "TENANT-A",
    }


def test_tenant_mismatch_fails_closed():
    engine = FakeEngine(
        principal_row={
            "tenant_id":
                "TENANT-A",
        },
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        PermissionError,
        match="tenant scope mismatch",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-B",
            principal_user_id=7,
        )

    assert len(
        engine.calls
    ) == 1


def test_missing_canonical_principal_fails_closed():
    engine = FakeEngine(
        principal_row=None,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        PermissionError,
        match="principal scope unavailable",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=7,
        )

    assert len(
        engine.calls
    ) == 1


@pytest.mark.parametrize(
    "principal_user_id",
    [
        0,
        -1,
        "",
        None,
        "not-an-int",
    ],
)
def test_invalid_principal_rejected(
    principal_user_id,
):
    engine = FakeEngine()

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        ValueError,
        match="positive integer",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=
                principal_user_id,
        )

    assert engine.calls == []


@pytest.mark.parametrize(
    "tenant_id",
    [
        "",
        "   ",
        None,
    ],
)
def test_invalid_tenant_rejected(
    tenant_id,
):
    engine = FakeEngine()

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        ValueError,
        match="non-empty",
    ):
        repository.list_for_principal(
            tenant_id=tenant_id,
            principal_user_id=7,
        )

    assert engine.calls == []


def test_repository_source_is_read_only():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/postgres/reports_repository.py"
    ).read_text()

    upper = source.upper()

    assert (
        "FROM PUBLIC.REPORTS AS R"
        in upper
    )

    assert (
        "WHERE H.TENANT_ID = :TENANT_ID"
        in upper
    )

    for forbidden in (
        "INSERT INTO PUBLIC.REPORTS",
        "UPDATE PUBLIC.REPORTS",
        "DELETE FROM PUBLIC.REPORTS",
    ):
        assert forbidden not in upper
