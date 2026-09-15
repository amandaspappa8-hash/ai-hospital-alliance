import pytest

from backend.app.repositories.postgres.medication_orders_repository import (
    PostgresMedicationOrdersRepository,
)


class FakeMappingsResult:
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
        tenant_id="tenant-1",
        hospital_id="hospital-1",
        user_id=7,
        medication_rows=None,
    ):
        self.tenant_id = tenant_id
        self.hospital_id = hospital_id
        self.user_id = user_id
        self.medication_rows = medication_rows or []
        self.statements = []
        self.parameters = []

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
        parameters=None,
    ):
        sql = str(statement)

        self.statements.append(sql)
        self.parameters.append(
            parameters or {}
        )

        if "FROM public.users AS u" in sql:
            return FakeMappingsResult(
                [
                    {
                        "user_id": self.user_id,
                        "hospital_id": self.hospital_id,
                        "tenant_id": self.tenant_id,
                    }
                ]
            )

        if (
            "FROM public.medication_orders_simple AS mo"
            in sql
        ):
            return FakeMappingsResult(
                self.medication_rows
            )

        raise AssertionError(
            f"Unexpected SQL: {sql}"
        )


class FakeEngine:
    def __init__(self, connection):
        self.connection = connection

    def connect(self):
        return self.connection


def _row():
    return {
        "id": 10,
        "patient_id": "P-001",
        "drug_name": "Example Drug",
        "generic_name": "Example Generic",
        "dose": "10 mg",
        "route": "PO",
        "frequency": "daily",
        "duration_days": 7,
        "quantity": 7,
        "is_active": True,
        "created_at": None,
    }


def test_list_for_principal_is_hospital_and_tenant_scoped():
    connection = FakeConnection(
        medication_rows=[_row()]
    )

    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(connection)
        )
    )

    rows = repository.list_for_principal(
        tenant_id="tenant-1",
        principal_user_id=7,
        limit=50,
    )

    assert rows == [_row()]

    collection_sql = next(
        sql
        for sql in connection.statements
        if "medication_orders_simple" in sql
    )

    assert (
        "JOIN public.patients AS p"
        in collection_sql
    )

    assert (
        "JOIN public.hospitals AS h"
        in collection_sql
    )

    assert (
        "p.hospital_id = :hospital_id"
        in collection_sql
    )

    assert (
        "h.tenant_id = :tenant_id"
        in collection_sql
    )

    collection_params = connection.parameters[-1]

    assert (
        collection_params["hospital_id"]
        == "hospital-1"
    )

    assert (
        collection_params["tenant_id"]
        == "tenant-1"
    )

    assert collection_params["limit"] == 50


def test_tenant_claim_mismatch_fails_closed():
    connection = FakeConnection(
        tenant_id="tenant-server"
    )

    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(connection)
        )
    )

    with pytest.raises(
        PermissionError,
        match="tenant does not match",
    ):
        repository.list_for_principal(
            tenant_id="tenant-client",
            principal_user_id=7,
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
    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(
                FakeConnection()
            )
        )
    )

    with pytest.raises(
        PermissionError
    ):
        repository.list_for_principal(
            tenant_id="tenant-1",
            principal_user_id=principal,
        )


@pytest.mark.parametrize(
    "limit",
    [
        0,
        51,
        -1,
        "abc",
    ],
)
def test_invalid_limit_rejected(
    limit,
):
    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(
                FakeConnection()
            )
        )
    )

    with pytest.raises(
        ValueError
    ):
        repository.list_for_principal(
            tenant_id="tenant-1",
            principal_user_id=7,
            limit=limit,
        )


class EmptyScopeConnection(FakeConnection):
    def execute(
        self,
        statement,
        parameters=None,
    ):
        sql = str(statement)

        self.statements.append(sql)
        self.parameters.append(
            parameters or {}
        )

        if "FROM public.users AS u" in sql:
            return FakeMappingsResult([])

        raise AssertionError(
            f"Unexpected SQL: {sql}"
        )


def test_unresolved_principal_scope_fails_closed():
    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(
                EmptyScopeConnection()
            )
        )
    )

    with pytest.raises(
        PermissionError,
        match="scope is unresolved",
    ):
        repository.list_for_principal(
            tenant_id="tenant-1",
            principal_user_id=7,
        )


class DuplicateScopeConnection(FakeConnection):
    def execute(
        self,
        statement,
        parameters=None,
    ):
        sql = str(statement)

        self.statements.append(sql)
        self.parameters.append(
            parameters or {}
        )

        if "FROM public.users AS u" in sql:
            return FakeMappingsResult(
                [
                    {
                        "user_id": 7,
                        "hospital_id": "hospital-1",
                        "tenant_id": "tenant-1",
                    },
                    {
                        "user_id": 7,
                        "hospital_id": "hospital-2",
                        "tenant_id": "tenant-1",
                    },
                ]
            )

        raise AssertionError(
            f"Unexpected SQL: {sql}"
        )


def test_ambiguous_principal_scope_fails_closed():
    repository = (
        PostgresMedicationOrdersRepository(
            FakeEngine(
                DuplicateScopeConnection()
            )
        )
    )

    with pytest.raises(
        PermissionError,
        match="scope is unresolved",
    ):
        repository.list_for_principal(
            tenant_id="tenant-1",
            principal_user_id=7,
        )
