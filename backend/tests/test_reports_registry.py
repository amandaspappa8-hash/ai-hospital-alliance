from __future__ import annotations

import pytest


REPORT_ENV_KEYS = (
    "AIHA_REPORTS_REPOSITORY",
    "AIHA_REPORTS_PG_HOST",
    "AIHA_REPORTS_PG_PORT",
    "AIHA_REPORTS_PG_DATABASE",
    "AIHA_REPORTS_PG_USER",
    "AIHA_REPORTS_PG_PASSWORD",
)


def _clear_reports_env(
    monkeypatch,
):
    for key in REPORT_ENV_KEYS:
        monkeypatch.delenv(
            key,
            raising=False,
        )


def test_reports_default_preserves_supplied_memory_store(
    monkeypatch,
):
    _clear_reports_env(
        monkeypatch
    )

    import backend.app.repositories.registry as registry

    store = [
        {
            "id": "R-LEGACY-1",
        }
    ]

    repository = (
        registry._build_reports_repository(
            store
        )
    )

    from backend.app.repositories.memory.reports_repository import (
        InMemoryReportsRepository,
    )

    assert isinstance(
        repository,
        InMemoryReportsRepository,
    )

    assert (
        repository.reports_store
        is store
    )


@pytest.mark.parametrize(
    "mode",
    [
        "",
        "memory",
        "inmemory",
        "in-memory",
    ],
)
def test_reports_memory_aliases(
    monkeypatch,
    mode,
):
    _clear_reports_env(
        monkeypatch
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_REPOSITORY",
        mode,
    )

    import backend.app.repositories.registry as registry

    store = [
        {
            "id": "R-1",
        }
    ]

    repository = (
        registry._build_reports_repository(
            store
        )
    )

    from backend.app.repositories.memory.reports_repository import (
        InMemoryReportsRepository,
    )

    assert isinstance(
        repository,
        InMemoryReportsRepository,
    )

    assert (
        repository.reports_store
        is store
    )


def test_reports_invalid_mode_fails_closed(
    monkeypatch,
):
    _clear_reports_env(
        monkeypatch
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_REPOSITORY",
        "sqlite",
    )

    import backend.app.repositories.registry as registry

    with pytest.raises(
        RuntimeError,
        match="Unsupported AIHA_REPORTS_REPOSITORY",
    ):
        registry._build_reports_repository(
            []
        )


def test_reports_postgres_requires_isolated_config(
    monkeypatch,
):
    _clear_reports_env(
        monkeypatch
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_REPOSITORY",
        "postgres",
    )

    import backend.app.repositories.registry as registry

    with pytest.raises(
        RuntimeError,
        match="Missing PostgreSQL Reports configuration",
    ):
        registry._build_reports_repository(
            []
        )


def test_reports_postgres_builder_uses_isolated_config(
    monkeypatch,
):
    _clear_reports_env(
        monkeypatch
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_REPOSITORY",
        "postgres",
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_PG_HOST",
        "127.0.0.1",
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_PG_PORT",
        "5432",
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_PG_DATABASE",
        "aiha_reports_test",
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_PG_USER",
        "reports_test",
    )

    monkeypatch.setenv(
        "AIHA_REPORTS_PG_PASSWORD",
        "secret",
    )

    import backend.app.repositories.registry as registry

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
        registry._build_reports_repository(
            [
                {
                    "id":
                        "SHOULD-NOT-BE-USED",
                }
            ]
        )
    )

    from backend.app.repositories.postgres.reports_repository import (
        PostgresReportsRepository,
    )

    assert isinstance(
        repository,
        PostgresReportsRepository,
    )

    assert repository._engine is fake_engine

    url = captured["url"]

    assert (
        url.drivername
        == "postgresql+psycopg2"
    )

    assert url.host == "127.0.0.1"
    assert url.port == 5432
    assert (
        url.database
        == "aiha_reports_test"
    )
    assert (
        url.username
        == "reports_test"
    )

    assert (
        captured["kwargs"]["future"]
        is True
    )

    assert (
        captured["kwargs"]["pool_pre_ping"]
        is True
    )


def test_registry_reports_binding_preserves_store_argument():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/registry.py"
    ).read_text()

    assert (
        '"reports": '
        '_build_reports_repository(reports_store or []),'
        in source
    )

    assert (
        '"reports": '
        'InMemoryReportsRepository(reports_store or []),'
        not in source
    )
