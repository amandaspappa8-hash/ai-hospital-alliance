from __future__ import annotations

from pathlib import Path

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
        scalar=None,
    ):
        self._one = one
        self._rows = rows or []
        self._scalar = scalar

    def mappings(self):
        return FakeMappingsResult(
            one=self._one,
            rows=self._rows,
        )

    def scalar_one_or_none(self):
        return self._scalar


class FakeConnection:
    def __init__(
        self,
        engine,
        *,
        transactional=False,
    ):
        self.engine = engine
        self.transactional = transactional
        self.connection_id = (
            engine.next_connection_id
        )

        engine.next_connection_id += 1

    def __enter__(self):
        if self.transactional:
            self.engine.begin_count += 1

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        if self.transactional:
            if exc_type is None:
                self.engine.commit_count += 1
            else:
                self.engine.rollback_count += 1

        return False

    def execute(
        self,
        statement,
        params,
    ):
        sql = str(
            statement
        )

        call = {
            "sql": sql,
            "params": dict(params),
            "connection_id":
                self.connection_id,
            "transactional":
                self.transactional,
        }

        self.engine.calls.append(
            call
        )

        if "FROM public.users AS u" in sql:
            return FakeExecuteResult(
                one=self.engine.principal_row
            )

        if "FROM public.reports AS r" in sql:
            return FakeExecuteResult(
                rows=self.engine.report_rows
            )

        if (
            "SELECT 1" in sql
            and "FROM public.patients AS p"
            in sql
        ):
            return FakeExecuteResult(
                scalar=(
                    1
                    if self.engine.patient_allowed
                    else None
                )
            )

        if "INSERT INTO public.reports" in sql:
            self.engine.insert_attempts += 1
            self.engine.insert_params.append(
                dict(params)
            )

            if self.engine.fail_insert:
                raise RuntimeError(
                    "synthetic insert failure"
                )

            if (
                self.engine.collision_attempts
                > 0
            ):
                self.engine.collision_attempts -= 1

                return FakeExecuteResult(
                    one=None
                )

            return FakeExecuteResult(
                one={
                    "id":
                        params["id"],
                    "patient_id":
                        params["patient_id"],
                    "title":
                        params["title"],
                    "type":
                        params["type"],
                    "status":
                        params["status"],
                    "body":
                        params["body"],
                    "summary":
                        params["summary"],
                }
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
        patient_allowed=True,
        collision_attempts=0,
        fail_insert=False,
    ):
        self.principal_row = (
            principal_row
        )

        self.report_rows = (
            report_rows
            or []
        )

        self.patient_allowed = (
            patient_allowed
        )

        self.collision_attempts = (
            collision_attempts
        )

        self.fail_insert = (
            fail_insert
        )

        self.calls = []
        self.insert_params = []

        self.insert_attempts = 0
        self.begin_count = 0
        self.commit_count = 0
        self.rollback_count = 0
        self.next_connection_id = 1

    def connect(self):
        return FakeConnection(
            self,
            transactional=False,
        )

    def begin(self):
        return FakeConnection(
            self,
            transactional=True,
        )


def _principal():
    return {
        "hospital_id": "HOSPITAL-A",
        "tenant_id": "TENANT-A",
    }


def _create(
    repository,
    *,
    tenant_id="TENANT-A",
    patient_id="P-1001",
    principal_user_id=7,
):
    return repository.create_for_principal(
        patient_id=patient_id,
        tenant_id=tenant_id,
        principal_user_id=
            principal_user_id,
        title="Clinical Report",
        report_type="Clinical",
        summary="Summary text",
        content="Body text",
        status="Ready",
    )


def test_list_for_principal_returns_canonical_contract():
    engine = FakeEngine(
        principal_row=_principal(),
        report_rows=[
            {
                "id": "R-1001",
                "patient_id": "P-1001",
                "title": "Clinical Report",
                "type": "Clinical",
                "status": "Ready",
                "body": "Body text",
            }
        ],
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    rows = repository.list_for_principal(
        tenant_id="TENANT-A",
        principal_user_id=7,
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

    assert len(engine.calls) == 2

    scope_sql = engine.calls[0]["sql"]
    reports_sql = engine.calls[1]["sql"]

    assert "FROM public.users AS u" in scope_sql
    assert "JOIN public.hospitals AS h" in scope_sql
    assert "JOIN public.tenants AS t" in scope_sql
    assert "u.is_active IS TRUE" in scope_sql

    assert "FROM public.reports AS r" in reports_sql
    assert "JOIN public.patients AS p" in reports_sql
    assert "JOIN public.hospitals AS h" in reports_sql
    assert (
        "WHERE p.hospital_id = :hospital_id"
        in reports_sql
    )
    assert (
        "AND h.tenant_id = :tenant_id"
        in reports_sql
    )


def test_tenant_mismatch_fails_closed():
    engine = FakeEngine(
        principal_row=_principal(),
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


def test_missing_principal_hospital_fails_closed():
    engine = FakeEngine(
        principal_row={
            "hospital_id": None,
            "tenant_id": "TENANT-A",
        },
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        PermissionError,
        match="principal hospital unavailable",
    ):
        repository.list_for_principal(
            tenant_id="TENANT-A",
            principal_user_id=7,
        )


def test_missing_canonical_principal_fails_closed():
    repository = (
        PostgresReportsRepository(
            FakeEngine(
                principal_row=None
            )
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


def test_create_for_principal_success():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    report = _create(
        repository
    )

    assert report["patient_id"] == "P-1001"
    assert report["title"] == "Clinical Report"
    assert report["type"] == "Clinical"
    assert report["summary"] == "Summary text"
    assert report["content"] == "Body text"
    assert report["status"] == "Ready"

    assert report["id"].startswith("R-")
    assert len(report["id"]) == 20

    assert engine.begin_count == 1
    assert engine.commit_count == 1
    assert engine.rollback_count == 0

    assert len(engine.calls) == 3

    connection_ids = {
        call["connection_id"]
        for call in engine.calls
    }

    assert len(connection_ids) == 1

    assert all(
        call["transactional"]
        for call in engine.calls
    )


def test_create_uses_principal_as_author_id():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    _create(
        repository,
        principal_user_id=7,
    )

    assert (
        engine.insert_params[0][
            "author_id"
        ]
        == 7
    )


def test_create_derives_hospital_server_side():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    _create(repository)

    patient_call = next(
        call
        for call in engine.calls
        if "FROM public.patients AS p"
        in call["sql"]
    )

    assert (
        patient_call["params"][
            "hospital_id"
        ]
        == "HOSPITAL-A"
    )

    assert (
        patient_call["params"][
            "tenant_id"
        ]
        == "TENANT-A"
    )


def test_create_tenant_claim_mismatch_denied():
    engine = FakeEngine(
        principal_row=_principal(),
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
        _create(
            repository,
            tenant_id="TENANT-B",
        )

    assert engine.insert_attempts == 0
    assert engine.commit_count == 0
    assert engine.rollback_count == 1


def test_create_cross_hospital_patient_denied():
    engine = FakeEngine(
        principal_row=_principal(),
        patient_allowed=False,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        PermissionError,
        match="outside authenticated",
    ):
        _create(repository)

    assert engine.insert_attempts == 0
    assert engine.rollback_count == 1


def test_create_patient_scope_sql_contains_tenant_and_hospital():
    engine = FakeEngine(
        principal_row=_principal(),
        patient_allowed=False,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(PermissionError):
        _create(repository)

    patient_sql = next(
        call["sql"]
        for call in engine.calls
        if "FROM public.patients AS p"
        in call["sql"]
    )

    assert "p.id = :patient_id" in patient_sql

    assert (
        "p.hospital_id = :hospital_id"
        in patient_sql
    )

    assert (
        "h.tenant_id = :tenant_id"
        in patient_sql
    )


def test_create_summary_and_content_storage_mapping():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    report = _create(repository)

    params = engine.insert_params[0]

    assert params["summary"] == "Summary text"
    assert params["body"] == "Body text"

    assert report["summary"] == "Summary text"
    assert report["content"] == "Body text"


def test_create_id_is_varchar20_compatible():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    report = _create(repository)

    assert report["id"].startswith("R-")
    assert len(report["id"]) == 20

    suffix = report["id"][2:]

    assert len(suffix) == 18

    allowed = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789-_"
    )

    assert all(
        char in allowed
        for char in suffix
    )


def test_create_retries_id_collision():
    engine = FakeEngine(
        principal_row=_principal(),
        collision_attempts=2,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    report = _create(repository)

    assert report["id"].startswith("R-")
    assert engine.insert_attempts == 3
    assert engine.commit_count == 1
    assert engine.rollback_count == 0


def test_create_collision_exhaustion_fails_closed():
    engine = FakeEngine(
        principal_row=_principal(),
        collision_attempts=10,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        RuntimeError,
        match="allocate unique report id",
    ):
        _create(repository)

    assert (
        engine.insert_attempts
        == repository._REPORT_ID_ATTEMPTS
    )

    assert engine.commit_count == 0
    assert engine.rollback_count == 1


def test_create_rolls_back_on_insert_failure():
    engine = FakeEngine(
        principal_row=_principal(),
        fail_insert=True,
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    with pytest.raises(
        RuntimeError,
        match="synthetic insert failure",
    ):
        _create(repository)

    assert engine.commit_count == 0
    assert engine.rollback_count == 1


def test_repository_source_has_scoped_canonical_writer():
    source = Path(
        "backend/app/repositories/postgres/"
        "reports_repository.py"
    ).read_text(
        encoding="utf-8"
    )

    upper = source.upper()

    assert (
        "INSERT INTO PUBLIC.REPORTS"
        in upper
    )

    assert (
        "ON CONFLICT (ID) DO NOTHING"
        in upper
    )

    assert (
        "FROM PUBLIC.USERS AS U"
        in upper
    )

    assert (
        "FROM PUBLIC.PATIENTS AS P"
        in upper
    )

    assert (
        "P.HOSPITAL_ID = :HOSPITAL_ID"
        in upper
    )

    assert (
        "H.TENANT_ID = :TENANT_ID"
        in upper
    )

    assert (
        "WITH SELF._ENGINE.BEGIN() "
        "AS CONNECTION"
        in upper
    )

    assert "LEN(REPORTS)" not in upper


def test_create_patient_scope_locks_authorized_patient_row():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    _create(repository)

    patient_call = next(
        call
        for call in engine.calls
        if "FROM public.patients AS p"
        in call["sql"]
    )

    normalized = " ".join(
        patient_call["sql"]
        .upper()
        .split()
    )

    assert (
        "FOR SHARE OF P, H"
        in normalized
    )

    assert (
        patient_call["transactional"]
        is True
    )

    insert_call = next(
        call
        for call in engine.calls
        if "INSERT INTO public.reports"
        in call["sql"]
    )

    assert (
        patient_call["connection_id"]
        == insert_call["connection_id"]
    )



def test_create_locks_principal_authority_rows():
    engine = FakeEngine(
        principal_row=_principal(),
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    _create(repository)

    scope_call = next(
        call
        for call in engine.calls
        if "FROM public.users AS u"
        in call["sql"]
    )

    normalized = " ".join(
        scope_call["sql"]
        .upper()
        .split()
    )

    assert (
        "FOR SHARE OF U, H"
        in normalized
    )

    assert (
        scope_call["transactional"]
        is True
    )

    patient_call = next(
        call
        for call in engine.calls
        if "FROM public.patients AS p"
        in call["sql"]
    )

    insert_call = next(
        call
        for call in engine.calls
        if "INSERT INTO public.reports"
        in call["sql"]
    )

    assert (
        scope_call["connection_id"]
        == patient_call["connection_id"]
        == insert_call["connection_id"]
    )


def test_list_principal_scope_does_not_take_writer_lock():
    engine = FakeEngine(
        principal_row=_principal(),
        report_rows=[],
    )

    repository = (
        PostgresReportsRepository(
            engine
        )
    )

    repository.list_for_principal(
        tenant_id="TENANT-A",
        principal_user_id=7,
    )

    scope_call = next(
        call
        for call in engine.calls
        if "FROM public.users AS u"
        in call["sql"]
    )

    normalized = " ".join(
        scope_call["sql"]
        .upper()
        .split()
    )

    assert (
        "FOR SHARE OF U, H"
        not in normalized
    )

    assert (
        scope_call["transactional"]
        is False
    )
