from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from backend.app.db.canonical_postgres import (
    build_canonical_postgres_url,
    get_canonical_postgres_engine,
    validate_canonical_postgres_environment,
)
from backend.app.repositories.postgres.saas_registration_repository import (
    PostgresCanonicalSaaSRegistrationRepository,
)


class _ScalarResult:
    def __init__(self, value):
        self._value = value

    def scalar_one(self):
        return self._value


class _MappingResult:
    def __init__(self, value):
        self._value = value

    def mappings(self):
        return self

    def one(self):
        return self._value


def _repository():
    return PostgresCanonicalSaaSRegistrationRepository(
        MagicMock()
    )


def _set_valid_environment(monkeypatch):
    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_HOST",
        "127.0.0.1",
    )
    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_PORT",
        "5432",
    )
    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_DATABASE",
        "aiha_db",
    )
    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_USER",
        "aiha",
    )
    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_PASSWORD",
        "unit-test-secret",
    )


def test_environment_fails_closed(monkeypatch):
    for name in (
        "AIHA_CANONICAL_PG_HOST",
        "AIHA_CANONICAL_PG_PORT",
        "AIHA_CANONICAL_PG_DATABASE",
        "AIHA_CANONICAL_PG_USER",
        "AIHA_CANONICAL_PG_PASSWORD",
    ):
        monkeypatch.delenv(
            name,
            raising=False,
        )

    with pytest.raises(
        RuntimeError,
        match="Missing canonical PostgreSQL runtime configuration",
    ):
        validate_canonical_postgres_environment()


def test_environment_rejects_wrong_database(monkeypatch):
    _set_valid_environment(monkeypatch)

    monkeypatch.setenv(
        "AIHA_CANONICAL_PG_DATABASE",
        "not_aiha_db",
    )

    with pytest.raises(
        RuntimeError,
        match="must equal aiha_db",
    ):
        validate_canonical_postgres_environment()


def test_url_and_engine_are_canonical(monkeypatch):
    _set_valid_environment(monkeypatch)

    url = build_canonical_postgres_url()

    assert url.drivername == "postgresql+psycopg2"
    assert url.host == "127.0.0.1"
    assert url.port == 5432
    assert url.database == "aiha_db"
    assert url.username == "aiha"

    get_canonical_postgres_engine.cache_clear()

    engine = get_canonical_postgres_engine()

    assert engine.dialect.name == "postgresql"

    engine.dispose()

    get_canonical_postgres_engine.cache_clear()


def test_slug_exists_uses_caller_connection():
    repository = _repository()
    connection = MagicMock()

    connection.execute.return_value = _ScalarResult(
        True
    )

    assert repository.slug_exists(
        slug="hospital",
        connection=connection,
    ) is True

    connection.commit.assert_not_called()
    connection.rollback.assert_not_called()
    connection.close.assert_not_called()


def test_registration_records_preserve_canonical_graph():
    repository = _repository()
    connection = MagicMock()

    departments = [
        ("Emergency", "ER-ABCD"),
        ("ICU", "ICU-ABCD"),
        ("Cardiology", "CARD-ABCD"),
        ("Radiology", "RAD-ABCD"),
        ("General", "GEN-ABCD"),
    ]

    department_id = {"value": 100}

    def execute(statement, parameters):
        sql = str(statement)

        if "INSERT INTO public.tenants" in sql:
            return _MappingResult(
                {
                    "id": "H-1234ABCD",
                    "slug": "test-hospital",
                    "api_key": "aiha_test",
                }
            )

        if "INSERT INTO public.hospitals" in sql:
            assert (
                parameters["tenant_id"]
                == "H-1234ABCD"
            )

            return _MappingResult(
                {
                    "id": "H-1234ABCD",
                    "tenant_id": "H-1234ABCD",
                }
            )

        if "INSERT INTO public.departments" in sql:
            assert (
                parameters["hospital_id"]
                == "H-1234ABCD"
            )

            department_id["value"] += 1

            return _MappingResult(
                {
                    "id": department_id["value"],
                    "code": parameters["code"],
                    "hospital_id": "H-1234ABCD",
                }
            )

        if "INSERT INTO public.users" in sql:
            assert (
                parameters["hospital_id"]
                == "H-1234ABCD"
            )
            assert (
                parameters["password"]
                == "hashed-value"
            )

            return _MappingResult(
                {
                    "id": 900,
                    "username": "admin@example.invalid",
                    "hospital_id": "H-1234ABCD",
                }
            )

        raise AssertionError(
            f"Unexpected SQL: {sql}"
        )

    connection.execute.side_effect = execute

    result = repository.create_registration_records(
        tenant_id="H-1234ABCD",
        tenant_name="Test Hospital",
        slug="test-hospital",
        plan="trial",
        admin_email="admin@example.invalid",
        admin_name="Admin",
        country="SE",
        phone="+460000000",
        api_key="aiha_test",
        trial_ends_at=None,
        hospital_name="Test Hospital",
        hospital_address="SE",
        hospital_phone="+460000000",
        departments=departments,
        admin_username="admin@example.invalid",
        admin_password_hash="hashed-value",
        admin_display_name="Admin",
        admin_role="admin",
        connection=connection,
    )

    assert result["tenant_id"] == "H-1234ABCD"
    assert result["hospital_id"] == "H-1234ABCD"
    assert result["user_id"] == 900
    assert len(result["department_ids"]) == 5

    # tenant + hospital + five departments + user
    assert connection.execute.call_count == 8

    connection.commit.assert_not_called()
    connection.rollback.assert_not_called()
    connection.close.assert_not_called()


def test_registration_rejects_empty_departments():
    repository = _repository()
    connection = MagicMock()

    with pytest.raises(
        ValueError,
        match="departments must contain",
    ):
        repository.create_registration_records(
            tenant_id="H-1234ABCD",
            tenant_name="Test Hospital",
            slug="test-hospital",
            plan="trial",
            admin_email="admin@example.invalid",
            admin_name="Admin",
            country="SE",
            phone="",
            api_key="aiha_test",
            trial_ends_at=None,
            hospital_name="Test Hospital",
            hospital_address="SE",
            hospital_phone="",
            departments=[],
            admin_username="admin@example.invalid",
            admin_password_hash="hashed-value",
            admin_display_name="Admin",
            admin_role="admin",
            connection=connection,
        )

    connection.execute.assert_not_called()
