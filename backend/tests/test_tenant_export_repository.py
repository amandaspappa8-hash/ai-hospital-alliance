from backend.app.repositories.postgres.tenant_export_repository import (
    PostgresTenantExportRepository,
)


class _FakeInspector:
    _columns = {
        "tenants": (
            "id",
            "name",
            "api_key",
        ),
        "users": (
            "id",
            "hospital_id",
            "password",
        ),
        "refresh_tokens": (
            "id",
            "user_id",
            "token_hash",
        ),
    }

    def get_columns(
        self,
        table,
        schema=None,
    ):
        names = self._columns.get(
            table,
            (
                "id",
                "tenant_id",
                "hospital_id",
                "patient_id",
                "user_id",
                "report_id",
            ),
        )

        return [
            {
                "name": name,
            }
            for name in names
        ]


def _repo_without_init():
    repo = object.__new__(
        PostgresTenantExportRepository
    )

    repo._inspector = _FakeInspector()

    return repo


def test_export_whitelist_has_expected_41_tables():
    assert len(
        PostgresTenantExportRepository.TABLE_STRATEGIES
    ) == 41

    assert (
        "tenants"
        in PostgresTenantExportRepository.TABLE_STRATEGIES
    )

    assert (
        "patients"
        in PostgresTenantExportRepository.TABLE_STRATEGIES
    )

    assert (
        "audit_logs"
        in PostgresTenantExportRepository.TABLE_STRATEGIES
    )

    assert not any(
        table.startswith("ahos_28_")
        for table in (
            PostgresTenantExportRepository
            .TABLE_STRATEGIES
        )
    )


def test_secret_field_exclusions_are_explicit():
    rules = (
        PostgresTenantExportRepository
        .FIELD_EXCLUSIONS
    )

    assert rules["tenants"] == {
        "api_key"
    }

    assert rules["users"] == {
        "password"
    }

    assert "refresh_tokens" not in rules


def test_unknown_table_is_rejected():
    repo = _repo_without_init()

    try:
        repo._select_sql(
            "definitely_not_allowed"
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "unknown export table was accepted"
        )


def test_sql_strategies_are_select_only_and_tenant_scoped():
    repo = _repo_without_init()

    for table in (
        PostgresTenantExportRepository
        .export_tables()
    ):
        sql = repo._select_sql(
            table
        )

        upper = sql.upper()

        assert upper.lstrip().startswith(
            "SELECT"
        )

        assert "INSERT " not in upper
        assert "UPDATE " not in upper
        assert "DELETE " not in upper
        assert "DROP " not in upper
        assert "ALTER " not in upper

        assert ":tenant_id" in sql



def test_refresh_tokens_are_not_in_portable_export_whitelist():
    repo = _repo_without_init()

    assert (
        "refresh_tokens"
        not in repo.TABLE_STRATEGIES
    )

    try:
        repo._select_sql(
            "refresh_tokens"
        )
    except ValueError as exc:
        assert (
            "Tenant export table is not allowed: refresh_tokens"
            in str(exc)
        )
    else:
        raise AssertionError(
            "refresh_tokens unexpectedly remained portable"
        )


def test_report_integrity_uses_report_patient_hospital_chain():
    repo = _repo_without_init()

    for table in (
        "report_content_digests",
        "report_content_macs",
        "report_verification_events",
    ):
        sql = repo._select_sql(
            table
        )

        assert (
            "JOIN public.reports AS r"
            in sql
        )

        assert (
            "JOIN public.patients AS p"
            in sql
        )

        assert (
            "JOIN public.hospitals AS h"
            in sql
        )


def test_sensitive_fields_are_excluded_from_sql_projection():
    repo = _repo_without_init()

    sensitive = {
        "tenants": "api_key",
        "users": "password",
    }

    for table, field in sensitive.items():
        sql = repo._select_sql(
            table
        )

        assert "SELECT x.*" not in sql

        assert (
            f'x."{field}"'
            not in sql
        )



def test_sensitive_nonsecret_columns_remain_selected():
    repo = _repo_without_init()

    tenant_sql = repo._select_sql(
        "tenants"
    )

    user_sql = repo._select_sql(
        "users"
    )

    assert 'x."id"' in tenant_sql
    assert 'x."name"' in tenant_sql

    assert 'x."id"' in user_sql
    assert 'x."hospital_id"' in user_sql


def test_tenant_export_repository_shared_connection_does_not_reconnect():
    from unittest.mock import MagicMock

    from backend.app.repositories.postgres.tenant_export_repository import (
        PostgresTenantExportRepository,
    )

    engine = MagicMock()
    repository = PostgresTenantExportRepository.__new__(
        PostgresTenantExportRepository
    )
    repository.engine = engine

    connection = MagicMock()

    result = MagicMock()
    result.mappings.return_value.first.return_value = {
        "user_id": 1,
        "hospital_id": "H-1",
        "tenant_id": "T-1",
    }
    connection.execute.return_value = result

    scope = repository.resolve_scope(
        tenant_id="T-1",
        principal_user_id=1,
        connection=connection,
    )

    assert scope["tenant_id"] == "T-1"
    engine.connect.assert_not_called()
    connection.execute.assert_called_once()


def test_tenant_export_repository_shared_connection_hospital_ids():
    from unittest.mock import MagicMock

    from backend.app.repositories.postgres.tenant_export_repository import (
        PostgresTenantExportRepository,
    )

    repository = PostgresTenantExportRepository.__new__(
        PostgresTenantExportRepository
    )

    repository.engine = MagicMock()

    connection = MagicMock()

    scope_result = MagicMock()
    scope_result.mappings.return_value.first.return_value = {
        "user_id": 1,
        "hospital_id": "H-1",
        "tenant_id": "T-1",
    }

    hospital_result = MagicMock()
    hospital_result.scalars.return_value.all.return_value = [
        "H-1",
        "H-2",
    ]

    connection.execute.side_effect = [
        scope_result,
        hospital_result,
    ]

    result = repository.hospital_ids_for_principal(
        tenant_id="T-1",
        principal_user_id=1,
        connection=connection,
    )

    assert result == [
        "H-1",
        "H-2",
    ]

    repository.engine.connect.assert_not_called()

    assert connection.execute.call_count == 2



def test_tenant_export_projection_uses_caller_connection_inspector():
    from unittest.mock import MagicMock, patch

    from backend.app.repositories.postgres.tenant_export_repository import (
        PostgresTenantExportRepository,
    )

    repository = (
        PostgresTenantExportRepository.__new__(
            PostgresTenantExportRepository
        )
    )

    repository.engine = MagicMock()
    repository._inspector = MagicMock()

    connection = MagicMock()
    connection_inspector = MagicMock()

    connection_inspector.get_columns.return_value = [
        {
            "name": "id",
        },
        {
            "name": "password",
        },
    ]

    repository.FIELD_EXCLUSIONS = {
        "users": {
            "password",
        },
    }

    repository.TABLE_STRATEGIES = {
        "users": "VIA_HOSPITAL",
    }

    with patch(
        "backend.app.repositories.postgres."
        "tenant_export_repository.sa_inspect",
        return_value=connection_inspector,
    ) as inspect_mock:

        projection = (
            repository._select_projection(
                "users",
                connection=connection,
            )
        )

    inspect_mock.assert_called_once_with(
        connection
    )

    connection_inspector.get_columns.assert_called_once_with(
        "users",
        schema="public",
    )

    repository._inspector.get_columns.assert_not_called()

    assert projection == 'x."id"'



def test_tenant_export_excluded_tables_uses_caller_connection_inspector():
    from unittest.mock import MagicMock, patch

    from backend.app.repositories.postgres.tenant_export_repository import (
        PostgresTenantExportRepository,
    )

    repository = (
        PostgresTenantExportRepository.__new__(
            PostgresTenantExportRepository
        )
    )

    repository.engine = MagicMock()
    repository._inspector = MagicMock()

    connection = MagicMock()
    connection_inspector = MagicMock()

    connection_inspector.get_table_names.return_value = [
        "patients",
        "legacy_table",
    ]

    repository.TABLE_STRATEGIES = {
        "patients": "VIA_HOSPITAL",
    }

    repository.PLATFORM_INTERNAL_TABLES = set()

    with patch(
        "backend.app.repositories.postgres."
        "tenant_export_repository.sa_inspect",
        return_value=connection_inspector,
    ) as inspect_mock:

        result = repository.excluded_tables(
            connection=connection,
        )

    inspect_mock.assert_called_once_with(
        connection
    )

    connection_inspector.get_table_names.assert_called_once_with(
        schema="public",
    )

    repository._inspector.get_table_names.assert_not_called()

    assert result == [
        {
            "table": "legacy_table",
            "reason":
            "UNCLASSIFIED_NOT_WHITELISTED",
        },
    ]



def test_refresh_tokens_have_explicit_nonportable_exclusion_reason():
    from unittest.mock import MagicMock, patch

    from backend.app.repositories.postgres.tenant_export_repository import (
        PostgresTenantExportRepository,
    )

    repository = (
        PostgresTenantExportRepository.__new__(
            PostgresTenantExportRepository
        )
    )

    repository.engine = MagicMock()
    repository._inspector = MagicMock()

    connection = MagicMock()
    connection_inspector = MagicMock()

    connection_inspector.get_table_names.return_value = [
        "patients",
        "refresh_tokens",
    ]

    repository.TABLE_STRATEGIES = {
        "patients": "VIA_HOSPITAL",
    }

    repository.PORTABILITY_EXCLUDED_TABLES = {
        "refresh_tokens":
        "PLATFORM_AUTHENTICATION_SECURITY_STATE",
    }

    repository.PLATFORM_INTERNAL_TABLES = set()

    with patch(
        "backend.app.repositories.postgres."
        "tenant_export_repository.sa_inspect",
        return_value=connection_inspector,
    ):
        result = repository.excluded_tables(
            connection=connection,
        )

    assert result == [
        {
            "table": "refresh_tokens",
            "reason":
            "PLATFORM_AUTHENTICATION_SECURITY_STATE",
        },
    ]
