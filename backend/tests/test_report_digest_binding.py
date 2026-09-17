from __future__ import annotations

import ast
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

import pytest


PROJECT = Path(__file__).resolve().parents[2]

MAIN = PROJECT / "backend/app/main.py"
CONTRACT = (
    PROJECT
    / "backend/app/repositories/contracts/reports_repository.py"
)
POSTGRES = (
    PROJECT
    / "backend/app/repositories/postgres/reports_repository.py"
)


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _tree(path: Path) -> ast.Module:
    return ast.parse(
        _source(path),
        filename=str(path),
    )


def _top_function(
    path: Path,
    name: str,
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    source = _source(path)
    tree = ast.parse(source)

    matches = [
        node
        for node in tree.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
        and node.name == name
    ]

    assert len(matches) == 1

    return matches[0]


def _function_source(
    path: Path,
    name: str,
) -> str:
    source = _source(path)
    node = _top_function(path, name)

    result = ast.get_source_segment(
        source,
        node,
    )

    assert result is not None

    return result


def _class_methods(
    path: Path,
    class_name: str,
) -> dict[str, ast.AST]:
    tree = _tree(path)

    classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and node.name == class_name
    ]

    assert len(classes) == 1

    return {
        node.name: node
        for node in classes[0].body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }


def _canonical_digest(
    row: dict[str, Any],
) -> str:
    canonical = {
        "report_id": str(
            row["report_id"]
        ),
        "patient_id": str(
            row["patient_id"]
        ),
        "author_id": (
            None
            if row["author_id"] is None
            else int(row["author_id"])
        ),
        "title": str(
            row["title"] or ""
        ),
        "type": str(
            row["type"] or ""
        ),
        "status": str(
            row["status"] or ""
        ),
        "body": str(
            row["body"] or ""
        ),
        "summary": str(
            row["summary"] or ""
        ),
    }

    serialized = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(
        serialized
    ).hexdigest()


def test_contract_exposes_digest_capabilities():
    methods = _class_methods(
        CONTRACT,
        "ReportsRepositoryContract",
    )

    assert (
        "register_content_digest_for_principal"
        in methods
    )

    assert (
        "verify_content_digest_for_principal"
        in methods
    )


def test_postgres_exposes_digest_capabilities():
    methods = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )

    assert "_canonical_report_digest" in methods

    assert (
        "register_content_digest_for_principal"
        in methods
    )

    assert (
        "verify_content_digest_for_principal"
        in methods
    )


def test_legacy_memory_authority_removed():
    source = _source(MAIN)

    assert "REPORT_HASHES" not in source
    assert "generate_report_hash" not in source


def test_routes_preserve_paths_and_payload_parameter():
    source = _source(MAIN)

    expected = {
        "secure_report":
            "/secure-report/{report_id}",
        "verify_secure":
            "/verify-secure/{report_id}",
    }

    for name, path in expected.items():
        node = _top_function(
            MAIN,
            name,
        )

        args = [
            arg.arg
            for arg in node.args.args
        ]

        assert args == [
            "report_id",
            "payload",
            "request",
        ]

        decorators = [
            ast.get_source_segment(
                source,
                dec,
            )
            for dec in node.decorator_list
        ]

        assert (
            f'app.post("{path}")'
            in decorators
        )


def test_secure_route_requires_verified_principal_and_repo_capability():
    text = _function_source(
        MAIN,
        "secure_report",
    )

    assert (
        "get_verified_principal_tenant"
        in text
    )

    assert 'REPOSITORIES.get(' in text
    assert '"reports"' in text

    assert (
        "register_content_digest_for_principal"
        in text
    )

    assert "status_code=503" in text
    assert "status_code=403" in text
    assert "status_code=422" in text
    assert "status_code=409" in text


def test_verify_route_requires_verified_principal_and_repo_capability():
    text = _function_source(
        MAIN,
        "verify_secure",
    )

    assert (
        "get_verified_principal_tenant"
        in text
    )

    assert 'REPOSITORIES.get(' in text
    assert '"reports"' in text

    assert (
        "verify_content_digest_for_principal"
        in text
    )

    assert "status_code=503" in text
    assert "status_code=403" in text
    assert "status_code=422" in text


def test_legacy_payload_is_not_digest_authority():
    secure = _function_source(
        MAIN,
        "secure_report",
    )

    verify = _function_source(
        MAIN,
        "verify_secure",
    )

    assert "_ = payload" in secure
    assert "_ = payload" in verify

    assert "generate_report_hash(payload)" not in secure
    assert "generate_report_hash(payload)" not in verify

    postgres = _source(POSTGRES)

    assert "payload" not in postgres


def test_canonical_v1_is_deterministic_and_unicode_stable():
    row = {
        "report_id": "R-TEST-1",
        "patient_id": "P-1001",
        "author_id": 7,
        "title": "CT",
        "type": "Radiology",
        "status": "Final",
        "body": "تقرير طبي – medicinsk rapport",
        "summary": "Stable",
    }

    reordered = dict(
        reversed(
            list(row.items())
        )
    )

    first = _canonical_digest(row)
    second = _canonical_digest(reordered)

    assert first == second
    assert len(first) == 64
    assert first == first.lower()


def test_content_change_changes_digest():
    row = {
        "report_id": "R-TEST-1",
        "patient_id": "P-1001",
        "author_id": 7,
        "title": "CT",
        "type": "Radiology",
        "status": "Final",
        "body": "Original",
        "summary": "Stable",
    }

    changed = dict(row)
    changed["body"] = "Changed"

    assert (
        _canonical_digest(row)
        != _canonical_digest(changed)
    )


def test_postgres_canonicalization_matches_frozen_contract_for_authorized_row():
    source = _source(POSTGRES)

    assert (
        '"canonicalization_version":'
        in source
    )

    assert "AIHA_REPORT_DIGEST_V1" in source
    assert "sort_keys=True" in source
    assert 'separators=(",", ":")' in source
    assert "ensure_ascii=False" in source
    assert '.encode("utf-8")' in source
    assert "hashlib.sha256" in source

    # The authorization query is an INNER JOIN to patients.
    # Therefore an authorized canonical report row cannot
    # reach digest generation with patient_id NULL.
    assert "JOIN public.patients AS p" in source
    assert "ON p.id = r.patient_id" in source


def test_register_uses_one_transaction_and_scope_locks():
    source = _source(POSTGRES)

    method = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )[
        "register_content_digest_for_principal"
    ]

    text = ast.get_source_segment(
        source,
        method,
    )

    assert text is not None

    assert "self._engine.begin()" in text
    assert (
        "_resolve_principal_scope_on_connection"
        in text
    )
    assert "lock_scope=True" in text
    assert "FOR SHARE OF r, p, h" in text

    assert "public.reports" in text
    assert "public.patients" in text
    assert "public.hospitals" in text

    assert (
        "public.report_content_digests"
        in text
    )


def test_registration_is_non_overwriting_and_idempotent_by_design():
    source = _source(POSTGRES)

    method = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )[
        "register_content_digest_for_principal"
    ]

    text = ast.get_source_segment(
        source,
        method,
    )

    assert text is not None

    assert "ON CONFLICT" in text
    assert "DO NOTHING" in text
    assert "DO UPDATE" not in text
    assert "FileExistsError" in text


def test_verify_recomputes_server_content_and_constant_time_compares():
    source = _source(POSTGRES)

    method = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )[
        "verify_content_digest_for_principal"
    ]

    text = ast.get_source_segment(
        source,
        method,
    )

    assert text is not None

    assert (
        "_canonical_report_digest"
        in text
    )

    assert "hmac.compare_digest" in text

    assert (
        "public.report_content_digests"
        in text
    )

    assert "public.reports" in text


def test_no_baseline_semantic_is_none():
    source = _source(POSTGRES)

    method = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )[
        "verify_content_digest_for_principal"
    ]

    text = ast.get_source_segment(
        source,
        method,
    )

    assert text is not None

    assert "if baseline is None:" in text
    assert "return None" in text


def test_verify_legacy_presentation_semantics_preserved():
    text = _function_source(
        MAIN,
        "verify_secure",
    )

    assert '"status": "NOT FOUND"' in text
    assert '"status": "VALID"' in text
    assert '"security": "UNCHANGED"' in text
    assert '"status": "TAMPERED"' in text
    assert '"security": "DATA MODIFIED"' in text

    assert (
        "legacy presentation wording only"
        in text
    )


def test_digest_comparison_property():
    left = "a" * 64
    same = "a" * 64
    different = "b" * 64

    assert hmac.compare_digest(
        left,
        same,
    )

    assert not hmac.compare_digest(
        left,
        different,
    )

# SEC-S4E18A — canonical digest NULL semantics


def test_e18a_digest_canonicalizer_preserves_json_null_runtime():
    import hashlib
    import json

    from backend.app.repositories.postgres.reports_repository import (
        PostgresReportsRepository,
    )

    row_with_nulls = {
        "report_id": "R-E18A-NULL",
        "patient_id": None,
        "author_id": None,
        "title": None,
        "type": None,
        "status": None,
        "body": None,
        "summary": None,
    }

    canonical = {
        "report_id": "R-E18A-NULL",
        "patient_id": None,
        "author_id": None,
        "title": None,
        "type": None,
        "status": None,
        "body": None,
        "summary": None,
    }

    expected = hashlib.sha256(
        json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()

    actual = (
        PostgresReportsRepository
        ._canonical_report_digest(
            row_with_nulls
        )
    )

    assert actual == expected



def test_e18a_digest_distinguishes_null_from_empty_string():
    from backend.app.repositories.postgres.reports_repository import (
        PostgresReportsRepository,
    )

    null_row = {
        "report_id": "R-E18A-DIFF",
        "patient_id": None,
        "author_id": None,
        "title": None,
        "type": None,
        "status": None,
        "body": None,
        "summary": None,
    }

    empty_row = {
        "report_id": "R-E18A-DIFF",
        "patient_id": "",
        "author_id": None,
        "title": "",
        "type": "",
        "status": "",
        "body": "",
        "summary": "",
    }

    null_digest = (
        PostgresReportsRepository
        ._canonical_report_digest(
            null_row
        )
    )

    empty_digest = (
        PostgresReportsRepository
        ._canonical_report_digest(
            empty_row
        )
    )

    assert null_digest != empty_digest



def test_e18a_digest_source_has_no_null_collapse():
    source = _source(POSTGRES)

    methods = _class_methods(
        POSTGRES,
        "PostgresReportsRepository",
    )

    canonical = ast.get_source_segment(
        source,
        methods[
            "_canonical_report_digest"
        ],
    ) or ""

    register = ast.get_source_segment(
        source,
        methods[
            "register_content_digest_for_principal"
        ],
    ) or ""

    verify = ast.get_source_segment(
        source,
        methods[
            "verify_content_digest_for_principal"
        ],
    ) or ""

    assert 'or ""' not in canonical
    assert "COALESCE(" not in register
    assert "COALESCE(" not in verify

    for field in (
        "report_id",
        "patient_id",
        "author_id",
        "title",
        "type",
        "status",
        "body",
        "summary",
    ):
        assert (
            f'row["{field}"]'
            in canonical
        )


def test_blockchain_legacy_routes_use_canonical_digest_authority():
    import inspect

    from backend.app import main

    register_source = inspect.getsource(
        main.blockchain_register
    )

    verify_source = inspect.getsource(
        main.blockchain_verify
    )

    assert (
        "get_verified_principal_tenant"
        in register_source
    )
    assert (
        "register_content_digest_for_principal"
        in register_source
    )

    assert (
        "get_verified_principal_tenant"
        in verify_source
    )
    assert (
        "verify_content_digest_for_principal"
        in verify_source
    )

    assert "BLOCKCHAIN_LEDGER" not in register_source
    assert "BLOCKCHAIN_LEDGER" not in verify_source

    assert "hashlib.sha256" not in register_source
    assert "hashlib.sha256" not in verify_source


def test_blockchain_register_ignores_client_payload_as_integrity_authority(
    monkeypatch,
):
    from backend.app import main

    calls = []

    class _Repository:
        def register_content_digest_for_principal(
            self,
            *,
            report_id,
            tenant_id,
            principal_user_id,
        ):
            calls.append(
                {
                    "report_id": report_id,
                    "tenant_id": tenant_id,
                    "principal_user_id":
                        principal_user_id,
                }
            )

            return {
                "digest_hex": "a" * 64,
            }

    monkeypatch.setitem(
        main.REPOSITORIES,
        "reports",
        _Repository(),
    )

    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            2,
            "T-AIHA-7548C3579712",
        ),
    )

    result = main.blockchain_register(
        "R-controlled",
        {
            "client":
                "payload must not be authority",
        },
        object(),
    )

    assert calls == [
        {
            "report_id": "R-controlled",
            "tenant_id":
                "T-AIHA-7548C3579712",
            "principal_user_id": 2,
        }
    ]

    assert result == {
        "report_id": "R-controlled",
        "hash": "a" * 64,
        "blockchain": "registered",
    }


def test_blockchain_verify_uses_canonical_digest_result(
    monkeypatch,
):
    from backend.app import main

    calls = []

    class _Repository:
        def verify_content_digest_for_principal(
            self,
            *,
            report_id,
            tenant_id,
            principal_user_id,
        ):
            calls.append(
                (
                    report_id,
                    tenant_id,
                    principal_user_id,
                )
            )

            return {
                "matches": True,
            }

    monkeypatch.setitem(
        main.REPOSITORIES,
        "reports",
        _Repository(),
    )

    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            2,
            "T-AIHA-7548C3579712",
        ),
    )

    result = main.blockchain_verify(
        "R-controlled",
        {
            "client":
                "payload must not be authority",
        },
        object(),
    )

    assert calls == [
        (
            "R-controlled",
            "T-AIHA-7548C3579712",
            2,
        )
    ]

    assert result == {
        "status": "VALID",
        "layer": "BLOCKCHAIN",
    }
