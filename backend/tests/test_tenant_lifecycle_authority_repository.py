from unittest.mock import MagicMock

from backend.app.repositories.postgres.tenant_lifecycle_authority_repository import (
    PostgresTenantLifecycleAuthorityRepository,
)


def test_repository_returns_none_when_authority_is_absent():
    engine = MagicMock()
    connection = MagicMock()
    result = MagicMock()

    engine.connect.return_value.__enter__.return_value = (
        connection
    )

    result.mappings.return_value.all.return_value = []

    connection.execute.return_value = result

    repository = (
        PostgresTenantLifecycleAuthorityRepository(
            engine
        )
    )

    authority = repository.get_by_tenant_id(
        tenant_id="TEN-1"
    )

    assert authority is None

    engine.connect.assert_called_once_with()
    connection.execute.assert_called_once()


def test_repository_uses_caller_connection_without_reconnect():
    engine = MagicMock()
    connection = MagicMock()
    result = MagicMock()

    result.mappings.return_value.all.return_value = [
        {
            "tenant_id": "TEN-1",
            "lifecycle_state": "ACTIVE",
            "legal_hold_active": False,
            "legal_hold_reason": None,
            "legal_hold_set_at": None,
            "legal_hold_released_at": None,
            "retention_until": None,
            "offboarding_requested_at": None,
            "offboarding_approved_at": None,
            "archive_completed_at": None,
            "purge_eligible_at": None,
            "created_at": None,
            "updated_at": None,
        }
    ]

    connection.execute.return_value = result

    repository = (
        PostgresTenantLifecycleAuthorityRepository(
            engine
        )
    )

    authority = repository.get_by_tenant_id(
        tenant_id="TEN-1",
        connection=connection,
    )

    assert authority is not None
    assert authority["tenant_id"] == "TEN-1"

    engine.connect.assert_not_called()
    connection.execute.assert_called_once()


def test_repository_rejects_blank_tenant_id():
    repository = (
        PostgresTenantLifecycleAuthorityRepository(
            MagicMock()
        )
    )

    try:
        repository.get_by_tenant_id(
            tenant_id="   "
        )
    except ValueError as exc:
        assert (
            "tenant_id must be non-empty"
            in str(exc)
        )
    else:
        raise AssertionError(
            "blank tenant_id was accepted"
        )


def test_repository_fails_closed_on_nonunique_authority():
    engine = MagicMock()
    connection = MagicMock()
    result = MagicMock()

    engine.connect.return_value.__enter__.return_value = (
        connection
    )

    result.mappings.return_value.all.return_value = [
        {"tenant_id": "TEN-1"},
        {"tenant_id": "TEN-1"},
    ]

    connection.execute.return_value = result

    repository = (
        PostgresTenantLifecycleAuthorityRepository(
            engine
        )
    )

    try:
        repository.get_by_tenant_id(
            tenant_id="TEN-1"
        )
    except RuntimeError as exc:
        assert (
            "Lifecycle authority is not unique"
            in str(exc)
        )
    else:
        raise AssertionError(
            "nonunique lifecycle authority was accepted"
        )


def test_repository_sql_is_select_only():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/postgres/"
        "tenant_lifecycle_authority_repository.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "FROM public.tenant_data_lifecycle AS l" in source
    assert "WHERE l.tenant_id = :tenant_id" in source

    # No write API exists on this repository.
    cls = PostgresTenantLifecycleAuthorityRepository

    for forbidden_method in (
        "create",
        "insert",
        "update",
        "delete",
        "purge",
        "truncate",
        "initialize",
    ):
        assert not hasattr(
            cls,
            forbidden_method,
        )
