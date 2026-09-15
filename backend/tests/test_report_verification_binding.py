from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

import backend.app.main as main
from backend.app.repositories.memory.reports_repository import (
    InMemoryReportsRepository,
)
from backend.app.repositories.postgres.reports_repository import (
    PostgresReportsRepository,
)


# ======================================================================
# Fake PostgreSQL execution model
# ======================================================================


class _Mappings:
    def __init__(self, one=None):
        self._one = one

    def one_or_none(self):
        return self._one


class _Result:
    def __init__(
        self,
        *,
        one=None,
        scalar=None,
    ):
        self._one = one
        self._scalar = scalar

    def mappings(self):
        return _Mappings(
            one=self._one
        )

    def scalar_one_or_none(self):
        return self._scalar


class VerificationFakeConnection:
    def __init__(
        self,
        engine,
        *,
        transactional: bool,
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
        sql = str(statement)

        call = {
            "sql": sql,
            "params": dict(params),
            "transactional":
                self.transactional,
            "connection_id":
                self.connection_id,
        }

        self.engine.calls.append(call)

        # Canonical principal:
        # users -> hospitals -> tenants.
        if "FROM public.users AS u" in sql:
            return _Result(
                one=self.engine.principal_row
            )

        # Scoped report authority query.
        if (
            "SELECT 1" in sql
            and "FROM public.reports AS r" in sql
            and "JOIN public.patients AS p" in sql
        ):
            return _Result(
                scalar=(
                    1
                    if self.engine.report_allowed
                    else None
                )
            )

        # Canonical idempotent registration.
        if (
            "INSERT INTO public.report_verification_events"
            in sql
        ):
            report_id = params["report_id"]

            self.engine.insert_count += 1
            self.engine.insert_params.append(
                dict(params)
            )

            if report_id in self.engine.events:
                return _Result(
                    one=None
                )

            row = {
                "id":
                    self.engine.next_event_id,
                "report_id":
                    report_id,
                "verification_type":
                    "REGISTRATION",
                "status":
                    "REGISTERED",
                "verified_by_user_id":
                    params["verified_by_user_id"],
                "verified_at":
                    self.engine.server_now,
            }

            self.engine.next_event_id += 1
            self.engine.events[
                report_id
            ] = row

            return _Result(
                one=dict(row)
            )

        # Existing canonical registration event.
        if (
            "FROM public.report_verification_events"
            in sql
        ):
            row = self.engine.events.get(
                params["report_id"]
            )

            return _Result(
                one=(
                    dict(row)
                    if row is not None
                    else None
                )
            )

        raise AssertionError(
            "Unexpected SQL: "
            + sql
        )


class VerificationFakeEngine:
    def __init__(
        self,
        *,
        principal_row=None,
        report_allowed=True,
        events=None,
    ):
        self.principal_row = (
            principal_row
            if principal_row is not None
            else {
                "hospital_id":
                    "HOSPITAL-A",
                "tenant_id":
                    "TENANT-A",
            }
        )

        self.report_allowed = (
            report_allowed
        )

        self.events = dict(
            events or {}
        )

        self.calls = []
        self.insert_params = []

        self.insert_count = 0
        self.begin_count = 0
        self.commit_count = 0
        self.rollback_count = 0

        self.next_connection_id = 1
        self.next_event_id = 100

        self.server_now = datetime(
            2026,
            9,
            15,
            18,
            0,
            tzinfo=timezone.utc,
        )

    def begin(self):
        return VerificationFakeConnection(
            self,
            transactional=True,
        )

    def connect(self):
        return VerificationFakeConnection(
            self,
            transactional=False,
        )


def _repository(
    *,
    principal_row=None,
    report_allowed=True,
    events=None,
):
    engine = VerificationFakeEngine(
        principal_row=principal_row,
        report_allowed=report_allowed,
        events=events,
    )

    return (
        PostgresReportsRepository(
            engine
        ),
        engine,
    )


def _register(
    repository,
    *,
    report_id="R-VERIFY-0001",
    tenant_id="TENANT-A",
    principal_user_id=7,
):
    return (
        repository
        .register_verification_for_principal(
            report_id=report_id,
            tenant_id=tenant_id,
            principal_user_id=
                principal_user_id,
        )
    )


def _read(
    repository,
    *,
    report_id="R-VERIFY-0001",
    tenant_id="TENANT-A",
    principal_user_id=7,
):
    return (
        repository
        .get_verification_for_principal(
            report_id=report_id,
            tenant_id=tenant_id,
            principal_user_id=
                principal_user_id,
        )
    )


# ======================================================================
# Repository tests
# ======================================================================


def test_repository_same_scope_register():
    repository, engine = _repository()

    row = _register(
        repository
    )

    assert row["report_id"] == (
        "R-VERIFY-0001"
    )

    assert (
        row["verification_type"]
        == "REGISTRATION"
    )

    assert row["status"] == "REGISTERED"

    assert (
        row["verified_by_user_id"]
        == 7
    )

    assert (
        row["verified_at"]
        == engine.server_now
    )

    assert engine.begin_count == 1
    assert engine.commit_count == 1
    assert engine.rollback_count == 0


def test_repository_registration_uses_one_transaction():
    repository, engine = _repository()

    _register(repository)

    relevant = [
        call
        for call in engine.calls
        if (
            "FROM public.users AS u"
            in call["sql"]
            or
            (
                "FROM public.reports AS r"
                in call["sql"]
                and "SELECT 1"
                in call["sql"]
            )
            or
            "INSERT INTO public.report_verification_events"
            in call["sql"]
        )
    ]

    assert relevant

    assert all(
        call["transactional"]
        for call in relevant
    )

    assert len({
        call["connection_id"]
        for call in relevant
    }) == 1


def test_repository_idempotent_repeat():
    repository, engine = _repository()

    first = _register(repository)
    second = _register(repository)

    assert first["id"] == second["id"]

    assert len(engine.events) == 1

    assert (
        engine.events[
            "R-VERIFY-0001"
        ]["verified_by_user_id"]
        == 7
    )

    assert engine.insert_count == 2


def test_repository_cross_hospital_report_denied():
    repository, engine = _repository(
        report_allowed=False
    )

    with pytest.raises(
        PermissionError,
        match="outside authenticated",
    ):
        _register(repository)

    assert engine.events == {}
    assert engine.insert_count == 0
    assert engine.rollback_count == 1


def test_repository_cross_tenant_denied():
    repository, engine = _repository()

    with pytest.raises(
        PermissionError,
        match="tenant scope mismatch",
    ):
        _register(
            repository,
            tenant_id="TENANT-B",
        )

    assert engine.events == {}
    assert engine.insert_count == 0
    assert engine.rollback_count == 1


def test_repository_read_same_scope():
    event = {
        "id": 55,
        "report_id":
            "R-VERIFY-0001",
        "verification_type":
            "REGISTRATION",
        "status":
            "REGISTERED",
        "verified_by_user_id":
            7,
        "verified_at":
            datetime(
                2026,
                9,
                15,
                18,
                5,
                tzinfo=timezone.utc,
            ),
    }

    repository, _ = _repository(
        events={
            "R-VERIFY-0001":
                event,
        }
    )

    assert _read(repository) == event


def test_repository_missing_event_returns_none():
    repository, _ = _repository()

    assert _read(repository) is None


def test_repository_read_cross_hospital_denied():
    repository, _ = _repository(
        report_allowed=False
    )

    with pytest.raises(
        PermissionError,
        match="outside authenticated",
    ):
        _read(repository)


def test_repository_server_derives_actor():
    repository, engine = _repository()

    _register(
        repository,
        principal_user_id=42,
    )

    assert len(
        engine.insert_params
    ) == 1

    params = engine.insert_params[0]

    assert (
        params["verified_by_user_id"]
        == 42
    )

    assert "tenant_id" not in params
    assert "hospital_id" not in params


def test_repository_server_generates_timestamp():
    repository, engine = _repository()

    _register(repository)

    params = engine.insert_params[0]

    assert "verified_at" not in params

    insert_sql = next(
        call["sql"]
        for call in engine.calls
        if (
            "INSERT INTO public.report_verification_events"
            in call["sql"]
        )
    )

    # Column has PostgreSQL DEFAULT now().
    # Application intentionally omits verified_at.
    assert "verified_at" not in (
        params
    )

    assert (
        engine.events[
            "R-VERIFY-0001"
        ]["verified_at"]
        == engine.server_now
    )

    assert "verified_by_user_id" in insert_sql


def test_repository_writer_locks_scope_and_report_authority():
    repository, engine = _repository()

    _register(repository)

    principal_sql = next(
        call["sql"]
        for call in engine.calls
        if "FROM public.users AS u"
        in call["sql"]
    )

    report_sql = next(
        call["sql"]
        for call in engine.calls
        if (
            "FROM public.reports AS r"
            in call["sql"]
            and "SELECT 1"
            in call["sql"]
        )
    )

    assert (
        "FOR SHARE OF u, h"
        in principal_sql
    )

    assert (
        "FOR SHARE OF r, p, h"
        in report_sql
    )


def test_repository_read_has_no_writer_lock():
    repository, engine = _repository()

    _read(repository)

    relevant_sql = "\n".join(
        call["sql"]
        for call in engine.calls
    )

    assert (
        "FOR SHARE OF r, p, h"
        not in relevant_sql
    )


# ======================================================================
# Endpoint test repositories / helpers
# ======================================================================


client = TestClient(
    main.app,
    raise_server_exceptions=False,
)


def _token(
    *,
    user_id=7,
    tenant_id="TENANT-A",
):
    return main.create_access_token(
        {
            "sub": str(user_id),
            "tenant_id":
                tenant_id,
        }
    )


def _headers(
    *,
    user_id=7,
    tenant_id="TENANT-A",
):
    return {
        "Authorization":
            "Bearer "
            + _token(
                user_id=user_id,
                tenant_id=tenant_id,
            )
    }


class _ReportsRepositoryScope:
    def __init__(
        self,
        repository,
    ):
        self.repository = repository
        self.previous = None

    def __enter__(self):
        self.previous = (
            main.REPOSITORIES.get(
                "reports"
            )
        )

        main.REPOSITORIES[
            "reports"
        ] = self.repository

        return self.repository

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        main.REPOSITORIES[
            "reports"
        ] = self.previous

        return False


class CapturingVerificationRepository:
    def __init__(
        self,
        *,
        event=None,
    ):
        self.register_calls = []
        self.get_calls = []

        self.event = (
            event
            if event is not None
            else {
                "id": 1,
                "report_id":
                    "R-VERIFY-0001",
                "verification_type":
                    "REGISTRATION",
                "status":
                    "REGISTERED",
                "verified_by_user_id":
                    7,
                "verified_at":
                    datetime(
                        2026,
                        9,
                        15,
                        18,
                        0,
                        tzinfo=timezone.utc,
                    ),
            }
        )

    def register_verification_for_principal(
        self,
        **kwargs,
    ):
        self.register_calls.append(
            dict(kwargs)
        )

        return dict(self.event)

    def get_verification_for_principal(
        self,
        **kwargs,
    ):
        self.get_calls.append(
            dict(kwargs)
        )

        return (
            None
            if self.event is None
            else dict(self.event)
        )


class MissingVerificationRepository:
    def get_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        return None


class DeniedVerificationRepository:
    def register_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise PermissionError(
            "scope denied"
        )

    def get_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise PermissionError(
            "scope denied"
        )


class InvalidVerificationRepository:
    def register_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise ValueError(
            "invalid report"
        )

    def get_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise ValueError(
            "invalid report"
        )


class FailedVerificationRepository:
    def register_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise RuntimeError(
            "database unavailable"
        )

    def get_verification_for_principal(
        self,
        **kwargs,
    ):
        del kwargs
        raise RuntimeError(
            "database unavailable"
        )


# ======================================================================
# Endpoint tests
# ======================================================================


@pytest.mark.parametrize(
    (
        "method",
        "path",
    ),
    [
        (
            "post",
            "/verify/register/R-VERIFY-0001",
        ),
        (
            "get",
            "/verify/R-VERIFY-0001",
        ),
    ],
)
def test_verification_routes_anonymous_are_401(
    method,
    path,
):
    response = getattr(
        client,
        method,
    )(path)

    assert response.status_code == 401


@pytest.mark.parametrize(
    (
        "method",
        "path",
    ),
    [
        (
            "post",
            "/verify/register/R-VERIFY-0001",
        ),
        (
            "get",
            "/verify/R-VERIFY-0001",
        ),
    ],
)
def test_verification_memory_repository_fails_closed(
    method,
    path,
):
    with _ReportsRepositoryScope(
        InMemoryReportsRepository([])
    ):
        response = getattr(
            client,
            method,
        )(
            path,
            headers=_headers(),
        )

    assert response.status_code == 503

    assert (
        response.json()["detail"]
        ==
        "Canonical report verification "
        "repository unavailable"
    )


def test_register_endpoint_forwards_verified_authority():
    repository = (
        CapturingVerificationRepository()
    )

    with _ReportsRepositoryScope(
        repository
    ):
        response = client.post(
            "/verify/register/R-VERIFY-0001",
            headers=_headers(
                user_id=42,
                tenant_id="TENANT-A",
            ),
        )

    assert response.status_code == 200

    assert repository.register_calls == [
        {
            "report_id":
                "R-VERIFY-0001",
            "tenant_id":
                "TENANT-A",
            "principal_user_id":
                42,
        }
    ]

    assert response.json() == {
        "message":
            "Report registered",
        "report_id":
            "R-VERIFY-0001",
    }


def test_get_endpoint_forwards_verified_authority():
    repository = (
        CapturingVerificationRepository()
    )

    with _ReportsRepositoryScope(
        repository
    ):
        response = client.get(
            "/verify/R-VERIFY-0001",
            headers=_headers(
                user_id=42,
                tenant_id="TENANT-A",
            ),
        )

    assert response.status_code == 200

    assert repository.get_calls == [
        {
            "report_id":
                "R-VERIFY-0001",
            "tenant_id":
                "TENANT-A",
            "principal_user_id":
                42,
        }
    ]


@pytest.mark.parametrize(
    (
        "method",
        "path",
    ),
    [
        (
            "post",
            "/verify/register/R-VERIFY-0001",
        ),
        (
            "get",
            "/verify/R-VERIFY-0001",
        ),
    ],
)
def test_verification_permission_maps_403(
    method,
    path,
):
    with _ReportsRepositoryScope(
        DeniedVerificationRepository()
    ):
        response = getattr(
            client,
            method,
        )(
            path,
            headers=_headers(),
        )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == "Report verification scope denied"
    )


@pytest.mark.parametrize(
    (
        "method",
        "path",
    ),
    [
        (
            "post",
            "/verify/register/R-VERIFY-0001",
        ),
        (
            "get",
            "/verify/R-VERIFY-0001",
        ),
    ],
)
def test_verification_value_error_maps_422(
    method,
    path,
):
    with _ReportsRepositoryScope(
        InvalidVerificationRepository()
    ):
        response = getattr(
            client,
            method,
        )(
            path,
            headers=_headers(),
        )

    assert response.status_code == 422

    assert (
        response.json()["detail"]
        == "invalid report"
    )


@pytest.mark.parametrize(
    (
        "method",
        "path",
    ),
    [
        (
            "post",
            "/verify/register/R-VERIFY-0001",
        ),
        (
            "get",
            "/verify/R-VERIFY-0001",
        ),
    ],
)
def test_verification_runtime_error_maps_503(
    method,
    path,
):
    with _ReportsRepositoryScope(
        FailedVerificationRepository()
    ):
        response = getattr(
            client,
            method,
        )(
            path,
            headers=_headers(),
        )

    assert response.status_code == 503


def test_get_missing_event_maps_404():
    with _ReportsRepositoryScope(
        MissingVerificationRepository()
    ):
        response = client.get(
            "/verify/R-VERIFY-0001",
            headers=_headers(),
        )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Report not found or invalid"
    )


def test_get_success_contract():
    repository = (
        CapturingVerificationRepository()
    )

    with _ReportsRepositoryScope(
        repository
    ):
        response = client.get(
            "/verify/R-VERIFY-0001",
            headers=_headers(),
        )

    assert response.status_code == 200

    assert response.json() == {
        "report_id":
            "R-VERIFY-0001",
        "status":
            "VERIFIED",
        "source":
            "AI Hospital Alliance",
        "security":
            "AIHA canonical verification registration",
    }


def test_target_source_has_no_memory_authority():
    source = (
        __import__(
            "pathlib"
        )
        .Path(
            "backend/app/main.py"
        )
        .read_text(
            encoding="utf-8"
        )
    )

    assert "VERIFIED_REPORTS" not in source

    assert (
        "Blockchain-grade verification"
        not in source
    )


def test_openapi_contract_no_drift():
    schema = main.app.openapi()

    assert len(
        schema["paths"]
    ) == 2294

    operation_ids = []

    for methods in (
        schema["paths"].values()
    ):
        for method, operation in (
            methods.items()
        ):
            if method.lower() not in {
                "get",
                "post",
                "put",
                "patch",
                "delete",
                "options",
                "head",
            }:
                continue

            operation_ids.append(
                operation.get(
                    "operationId"
                )
            )

    operation_ids = [
        value
        for value in operation_ids
        if value
    ]

    assert len(operation_ids) == 2345

    assert (
        len(operation_ids)
        == len(set(operation_ids))
    )

    post = schema["paths"][
        "/verify/register/{report_id}"
    ]["post"]

    get = schema["paths"][
        "/verify/{report_id}"
    ]["get"]

    assert (
        post["operationId"]
        ==
        "register_report_verify_register__report_id__post"
    )

    assert (
        get["operationId"]
        ==
        "verify_report_verify__report_id__get"
    )
