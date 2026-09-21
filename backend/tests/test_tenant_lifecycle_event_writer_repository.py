from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.app.repositories.contracts.tenant_lifecycle_event_writer_repository import (
    TenantLifecycleEventWriterRepositoryContract,
)
from backend.app.repositories.postgres.tenant_lifecycle_event_writer_repository import (
    PostgresTenantLifecycleEventWriterRepository,
)


POSTGRES_SOURCE = Path(
    "backend/app/repositories/postgres/"
    "tenant_lifecycle_event_writer_repository.py"
)


def _result_row():
    return {
        "id": 101,
        "tenant_id": "TEN-1",
        "event_type": "future_event_v2",
        "actor_user_id": 7,
        "reason": "test reason",
        "occurred_at": object(),
        "metadata": {"source": "test"},
    }


def _mock_mapping_result(row=None):
    result = MagicMock()
    mappings = MagicMock()

    result.mappings.return_value = mappings
    mappings.one.return_value = (
        row
        if row is not None
        else _result_row()
    )

    return result


def test_contract_exposes_append_event():
    assert hasattr(
        TenantLifecycleEventWriterRepositoryContract,
        "append_event",
    )


def test_repository_owned_transaction_uses_engine_begin():
    engine = MagicMock()
    connection = MagicMock()

    engine.begin.return_value.__enter__.return_value = (
        connection
    )
    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    result = repository.append_event(
        tenant_id="TEN-1",
        event_type="future_event_v2",
        actor_user_id=7,
        reason="test reason",
        metadata={"source": "test"},
    )

    engine.begin.assert_called_once_with()
    connection.execute.assert_called_once()
    assert result["id"] == 101
    assert result["event_type"] == "future_event_v2"


def test_caller_connection_is_used_without_repository_transaction_control():
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    repository.append_event(
        tenant_id="TEN-1",
        event_type="future_event_v2",
        connection=connection,
    )

    engine.begin.assert_not_called()
    connection.execute.assert_called_once()
    connection.commit.assert_not_called()
    connection.rollback.assert_not_called()
    connection.close.assert_not_called()


def test_writer_sql_is_insert_only_and_targets_exact_table():
    source = POSTGRES_SOURCE.read_text(
        encoding="utf-8"
    )

    assert (
        "INSERT INTO public.tenant_data_lifecycle_events"
        in source
    )

    upper_source = source.upper()

    assert (
        "UPDATE PUBLIC.TENANT_DATA_LIFECYCLE_EVENTS"
        not in upper_source
    )
    assert (
        "DELETE FROM PUBLIC.TENANT_DATA_LIFECYCLE_EVENTS"
        not in upper_source
    )
    assert (
        "TRUNCATE PUBLIC.TENANT_DATA_LIFECYCLE_EVENTS"
        not in upper_source
    )


def test_insert_omits_id_and_occurred_at_from_insert_columns():
    source = POSTGRES_SOURCE.read_text(
        encoding="utf-8"
    )

    insert_start = source.index(
        "INSERT INTO public.tenant_data_lifecycle_events"
    )
    values_start = source.index(
        "VALUES",
        insert_start,
    )

    insert_columns = source[
        insert_start:values_start
    ]

    assert "\n                id," not in insert_columns
    assert "occurred_at" not in insert_columns


def test_insert_returns_all_authoritative_fields():
    source = POSTGRES_SOURCE.read_text(
        encoding="utf-8"
    )

    returning = source.split(
        "RETURNING",
        1,
    )[1]

    for field in (
        "id",
        "tenant_id",
        "event_type",
        "actor_user_id",
        "reason",
        "occurred_at",
        "metadata",
    ):
        assert field in returning


def test_repository_returns_persisted_row_dict():
    engine = MagicMock()
    connection = MagicMock()

    persisted = _result_row()

    connection.execute.return_value = (
        _mock_mapping_result(
            persisted
        )
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    result = repository.append_event(
        tenant_id="TEN-1",
        event_type="future_event_v2",
        connection=connection,
    )

    assert result == persisted
    assert result is not persisted


def test_event_type_is_not_enumerated():
    source = POSTGRES_SOURCE.read_text(
        encoding="utf-8"
    )

    assert "event_type IN (" not in source
    assert "event_type in (" not in source


@pytest.mark.parametrize(
    "event_type",
    [
        "future_event_v2",
        "lowercase_event",
        "  event_name  ",
        "",
        "   ",
        "\t",
        "\n",
    ],
)
def test_event_type_is_passed_without_normalization(
    event_type,
):
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    repository.append_event(
        tenant_id="TEN-1",
        event_type=event_type,
        connection=connection,
    )

    parameters = (
        connection.execute.call_args.args[1]
    )

    assert parameters["event_type"] == event_type


def test_metadata_is_serialized_as_json():
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    repository.append_event(
        tenant_id="TEN-1",
        event_type="future_event",
        metadata={
            "source": "P21",
            "nested": {"enabled": True},
        },
        connection=connection,
    )

    parameters = (
        connection.execute.call_args.args[1]
    )

    assert json.loads(
        parameters["metadata"]
    ) == {
        "source": "P21",
        "nested": {"enabled": True},
    }


def test_none_metadata_remains_none():
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    repository.append_event(
        tenant_id="TEN-1",
        event_type="future_event",
        metadata=None,
        connection=connection,
    )

    parameters = (
        connection.execute.call_args.args[1]
    )

    assert parameters["metadata"] is None


def test_blank_event_type_is_not_replaced_by_writer():
    engine = MagicMock()
    connection = MagicMock()

    connection.execute.return_value = (
        _mock_mapping_result()
    )

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    repository.append_event(
        tenant_id="TEN-1",
        event_type="   ",
        connection=connection,
    )

    parameters = (
        connection.execute.call_args.args[1]
    )

    assert parameters["event_type"] == "   "


def test_blank_tenant_id_is_rejected_before_sql():
    engine = MagicMock()
    connection = MagicMock()

    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            engine
        )
    )

    with pytest.raises(
        ValueError,
        match="tenant_id must be non-empty",
    ):
        repository.append_event(
            tenant_id="   ",
            event_type="future_event",
            connection=connection,
        )

    connection.execute.assert_not_called()


def test_invalid_event_type_type_is_rejected():
    repository = (
        PostgresTenantLifecycleEventWriterRepository(
            MagicMock()
        )
    )

    with pytest.raises(
        TypeError,
        match="event_type must be a string",
    ):
        repository.append_event(
            tenant_id="TEN-1",
            event_type=123,  # type: ignore[arg-type]
            connection=MagicMock(),
        )
