from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from backend.app.repositories.postgres.tenant_lifecycle_mutation_repository import (
    PostgresTenantLifecycleMutationRepository,
)


class _MappingResult:
    def __init__(self, value):
        self._value = value

    def mappings(self):
        return self

    def one(self):
        return self._value


def test_create_initial_lifecycle_uses_caller_connection_only():
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = _MappingResult(
        {
            "tenant_id": "H-1234ABCD",
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
    )

    repository = PostgresTenantLifecycleMutationRepository(
        engine
    )

    result = repository.create_initial_lifecycle(
        tenant_id="H-1234ABCD",
        lifecycle_state="ACTIVE",
        connection=connection,
    )

    assert result["tenant_id"] == "H-1234ABCD"
    assert result["lifecycle_state"] == "ACTIVE"
    assert result["legal_hold_active"] is False

    connection.commit.assert_not_called()
    connection.rollback.assert_not_called()
    connection.close.assert_not_called()

    engine.begin.assert_not_called()
    engine.connect.assert_not_called()


def test_rejects_blank_tenant():
    repository = PostgresTenantLifecycleMutationRepository(
        MagicMock()
    )

    with pytest.raises(
        ValueError,
        match="tenant_id",
    ):
        repository.create_initial_lifecycle(
            tenant_id=" ",
            lifecycle_state="ACTIVE",
            connection=MagicMock(),
        )


def test_rejects_blank_lifecycle_state():
    repository = PostgresTenantLifecycleMutationRepository(
        MagicMock()
    )

    with pytest.raises(
        ValueError,
        match="lifecycle_state",
    ):
        repository.create_initial_lifecycle(
            tenant_id="H-1234ABCD",
            lifecycle_state=" ",
            connection=MagicMock(),
        )
