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


def test_export_whitelist_has_expected_42_tables():
    assert len(
        PostgresTenantExportRepository.TABLE_STRATEGIES
    ) == 42

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

    assert rules["refresh_tokens"] == {
        "token_hash"
    }


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


def test_refresh_tokens_use_safe_text_side_join():
    repo = _repo_without_init()

    sql = repo._select_sql(
        "refresh_tokens"
    )

    assert (
        "u.id::text = BTRIM(x.user_id)"
        in sql
    )

    assert (
        "x.user_id::integer"
        not in sql.lower()
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
        "refresh_tokens": "token_hash",
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

    refresh_sql = repo._select_sql(
        "refresh_tokens"
    )

    assert 'x."id"' in tenant_sql
    assert 'x."name"' in tenant_sql

    assert 'x."id"' in user_sql
    assert 'x."hospital_id"' in user_sql

    assert 'x."id"' in refresh_sql
    assert 'x."user_id"' in refresh_sql
