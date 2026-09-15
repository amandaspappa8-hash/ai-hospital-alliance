import pytest

from backend.app.repositories import registry
from backend.app.repositories.postgres.medication_orders_repository import (
    PostgresMedicationOrdersRepository,
)


PG_KEYS = {
    "AIHA_MEDICATION_ORDERS_PG_HOST": "127.0.0.1",
    "AIHA_MEDICATION_ORDERS_PG_PORT": "5432",
    "AIHA_MEDICATION_ORDERS_PG_DATABASE": "aiha_db",
    "AIHA_MEDICATION_ORDERS_PG_USER": "aiha",
    "AIHA_MEDICATION_ORDERS_PG_PASSWORD": "test-only",
}


def _clear(monkeypatch):
    monkeypatch.delenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        raising=False,
    )

    for key in PG_KEYS:
        monkeypatch.delenv(
            key,
            raising=False,
        )


def test_default_is_disabled(
    monkeypatch,
):
    _clear(monkeypatch)

    assert (
        registry._build_medication_orders_repository()
        is None
    )


def test_invalid_mode_fails_closed(
    monkeypatch,
):
    _clear(monkeypatch)

    monkeypatch.setenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        "memory",
    )

    with pytest.raises(
        RuntimeError,
        match="disabled.*postgres",
    ):
        registry._build_medication_orders_repository()


def test_postgres_requires_isolated_configuration(
    monkeypatch,
):
    _clear(monkeypatch)

    monkeypatch.setenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        "postgres",
    )

    with pytest.raises(
        RuntimeError,
        match="Missing isolated PostgreSQL Medication Orders",
    ):
        registry._build_medication_orders_repository()


def test_invalid_port_fails_closed(
    monkeypatch,
):
    _clear(monkeypatch)

    monkeypatch.setenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        "postgres",
    )

    for key, value in PG_KEYS.items():
        monkeypatch.setenv(
            key,
            value,
        )

    monkeypatch.setenv(
        "AIHA_MEDICATION_ORDERS_PG_PORT",
        "invalid",
    )

    with pytest.raises(
        RuntimeError,
        match="must be an integer",
    ):
        registry._build_medication_orders_repository()


def test_postgres_mode_builds_isolated_repository(
    monkeypatch,
):
    _clear(monkeypatch)

    monkeypatch.setenv(
        "AIHA_MEDICATION_ORDERS_REPOSITORY",
        "postgres",
    )

    for key, value in PG_KEYS.items():
        monkeypatch.setenv(
            key,
            value,
        )

    captured = {}

    class FakeEngine:
        pass

    fake_engine = FakeEngine()

    def fake_create_engine(
        url,
        **kwargs,
    ):
        captured["url"] = url
        captured["kwargs"] = kwargs
        return fake_engine

    monkeypatch.setattr(
        registry,
        "create_engine",
        fake_create_engine,
    )

    repository = (
        registry._build_medication_orders_repository()
    )

    assert isinstance(
        repository,
        PostgresMedicationOrdersRepository,
    )

    assert repository.engine is fake_engine

    url = captured["url"]

    assert (
        url.drivername
        == "postgresql+psycopg2"
    )
    assert url.host == "127.0.0.1"
    assert url.port == 5432
    assert url.database == "aiha_db"
    assert url.username == "aiha"

    assert (
        captured["kwargs"]["pool_pre_ping"]
        is True
    )


def test_build_repositories_contains_disabled_medication_orders(
    monkeypatch,
):
    _clear(monkeypatch)

    repositories = registry.build_repositories(
        users_store={},
        patients_store={},
        notes_store={},
        orders_store={},
    )

    assert "medication_orders" in repositories
    assert repositories["medication_orders"] is None


def test_build_repositories_calls_medication_orders_builder_once(
    monkeypatch,
):
    _clear(monkeypatch)

    sentinel = object()
    calls = []

    def fake_builder():
        calls.append(True)
        return sentinel

    monkeypatch.setattr(
        registry,
        "_build_medication_orders_repository",
        fake_builder,
    )

    repositories = registry.build_repositories(
        users_store={},
        patients_store={},
        notes_store={},
        orders_store={},
    )

    assert calls == [True]
    assert (
        repositories["medication_orders"]
        is sentinel
    )
