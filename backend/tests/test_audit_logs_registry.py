import pytest

import backend.app.repositories.registry as registry


AUDIT_ENV_KEYS = (
    "AIHA_AUDIT_LOGS_REPOSITORY",
    "AIHA_AUDIT_LOGS_PG_HOST",
    "AIHA_AUDIT_LOGS_PG_PORT",
    "AIHA_AUDIT_LOGS_PG_DATABASE",
    "AIHA_AUDIT_LOGS_PG_USER",
    "AIHA_AUDIT_LOGS_PG_PASSWORD",
)


def clear_audit_env(monkeypatch):
    for key in AUDIT_ENV_KEYS:
        monkeypatch.delenv(
            key,
            raising=False,
        )


def test_audit_logs_repository_default_is_disabled(
    monkeypatch,
):
    clear_audit_env(monkeypatch)

    assert (
        registry._build_audit_logs_repository()
        is None
    )


def test_invalid_audit_logs_repository_mode_fails_closed(
    monkeypatch,
):
    clear_audit_env(monkeypatch)

    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_REPOSITORY",
        "sqlite",
    )

    with pytest.raises(
        RuntimeError,
        match="disabled.*postgres",
    ):
        registry._build_audit_logs_repository()


def test_postgres_requires_isolated_configuration(
    monkeypatch,
):
    clear_audit_env(monkeypatch)

    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_REPOSITORY",
        "postgres",
    )

    with pytest.raises(
        RuntimeError,
        match="Missing isolated PostgreSQL Audit Logs",
    ):
        registry._build_audit_logs_repository()


def test_explicit_postgres_builds_repository(
    monkeypatch,
):
    clear_audit_env(monkeypatch)

    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_REPOSITORY",
        "postgres",
    )

    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_PG_HOST",
        "127.0.0.1",
    )
    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_PG_PORT",
        "5432",
    )
    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_PG_DATABASE",
        "aiha_db",
    )
    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_PG_USER",
        "aiha",
    )
    monkeypatch.setenv(
        "AIHA_AUDIT_LOGS_PG_PASSWORD",
        "secret",
    )

    captured = {}

    class SentinelRepository:
        def __init__(self, engine):
            captured["engine"] = engine

    def fake_create_engine(
        url,
        **kwargs,
    ):
        captured["url"] = url
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr(
        registry,
        "PostgresAuditLogsRepository",
        SentinelRepository,
    )

    monkeypatch.setattr(
        registry,
        "create_engine",
        fake_create_engine,
    )

    repository = (
        registry._build_audit_logs_repository()
    )

    assert isinstance(
        repository,
        SentinelRepository,
    )

    assert (
        captured["url"].drivername
        == "postgresql+psycopg2"
    )

    assert captured["url"].host == "127.0.0.1"
    assert captured["url"].port == 5432
    assert captured["url"].database == "aiha_db"
    assert captured["url"].username == "aiha"

    assert captured["kwargs"]["pool_pre_ping"] is True
