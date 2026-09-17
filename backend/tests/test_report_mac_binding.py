from __future__ import annotations

import ast
import hashlib
import hmac
import json
from pathlib import Path

import pytest
from fastapi import HTTPException

from backend.app.repositories.postgres.reports_repository import (
    PostgresReportsRepository,
)


PROJECT = Path(__file__).resolve().parents[2]

MAIN = PROJECT / "backend/app/main.py"

CONTRACT = (
    PROJECT
    / "backend/app/repositories/contracts/"
      "reports_repository.py"
)

REPOSITORY = (
    PROJECT
    / "backend/app/repositories/postgres/"
      "reports_repository.py"
)


def _function_source(
    path: Path,
    name: str,
) -> str:
    source = path.read_text(
        encoding="utf-8",
    )

    tree = ast.parse(source)

    matches = [
        node
        for node in ast.walk(tree)
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name == name
        )
    ]

    assert len(matches) == 1, (
        name,
        [
            (
                node.lineno,
                getattr(
                    node,
                    "end_lineno",
                    None,
                ),
            )
            for node in matches
        ],
    )

    return (
        ast.get_source_segment(
            source,
            matches[0],
        )
        or ""
    )



def test_contract_has_mac_methods():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/contracts/"
        "reports_repository.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "register_content_mac_for_principal" in source
    assert "verify_content_mac_for_principal" in source
    assert "active_key_id: str" in source
    assert "mac_key_resolver" in source
    assert "mac_key: bytes" not in source


def test_repository_mac_primitives():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/postgres/"
        "reports_repository.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "AIHA_REPORT_CONTENT_MAC_V1" in source
    assert "HMAC-SHA256" in source
    assert "hmac.new" in source
    assert "hmac.compare_digest" in source
    assert "active_key_id" in source
    assert "mac_key_resolver" in source
    assert '"key_id"' in source
    assert ":key_id" in source


def test_canonical_mac_preserves_null():
    row = {
        "report_id": "R-NULL",
        "patient_id": None,
        "author_id": None,
        "title": None,
        "type": None,
        "status": None,
        "body": None,
        "summary": None,
    }

    key = b"mac-test-key"

    canonical = {
        "mac_version":
            "AIHA_REPORT_CONTENT_MAC_V1",
        "report_id":
            "R-NULL",
        "patient_id":
            None,
        "author_id":
            None,
        "title":
            None,
        "type":
            None,
        "status":
            None,
        "body":
            None,
        "summary":
            None,
    }

    expected = hmac.new(
        key,
        json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    actual = (
        PostgresReportsRepository
        ._canonical_report_mac(
            row,
            key,
        )
    )

    assert actual == expected
    assert len(actual) == 64


def test_report_id_is_mac_bound():
    key = b"mac-test-key"

    first = {
        "report_id": "R-1",
        "patient_id": "P-1",
        "author_id": 1,
        "title": None,
        "type": None,
        "status": None,
        "body": None,
        "summary": None,
    }

    second = dict(first)
    second["report_id"] = "R-2"

    assert (
        PostgresReportsRepository
        ._canonical_report_mac(
            first,
            key,
        )
        !=
        PostgresReportsRepository
        ._canonical_report_mac(
            second,
            key,
        )
    )


def test_routes_use_canonical_reports_repository():
    from pathlib import Path

    source = Path(
        "backend/app/main.py"
    ).read_text(
        encoding="utf-8"
    )

    assert "register_content_mac_for_principal" in source
    assert "verify_content_mac_for_principal" in source
    assert "AIHA_REPORT_MAC_ACTIVE_KEY_ID" in source
    assert "AIHA_REPORT_MAC_KEYS_JSON" in source
    assert "mac_key_resolver=" in source


def test_client_payload_signature_not_authority():
    source = MAIN.read_text(
        encoding="utf-8",
    )

    tree = ast.parse(source)

    functions = {
        n.name: n
        for n in tree.body
        if isinstance(
            n,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    checks = {
        "sign_report":
            {"payload"},
        "verify_report_signature":
            {
                "payload",
                "signature",
            },
    }

    for name, forbidden in checks.items():

        loads = {
            n.id
            for n in ast.walk(
                functions[name]
            )
            if (
                isinstance(n, ast.Name)
                and isinstance(
                    n.ctx,
                    ast.Load,
                )
            )
        }

        assert not (
            loads & forbidden
        )


def test_dedicated_key_fails_closed(monkeypatch):
    from fastapi import HTTPException
    from backend.app import main

    monkeypatch.delenv(
        "AIHA_REPORT_MAC_ACTIVE_KEY_ID",
        raising=False,
    )
    monkeypatch.delenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        raising=False,
    )

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_KEY",
        "must-not-work",
    )
    monkeypatch.setenv(
        "SECRET_KEY",
        "must-not-work",
    )

    try:
        main._get_active_report_mac_key_id()
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError(
            "legacy key unexpectedly became fallback"
        )


def test_dedicated_key_returns_bytes(monkeypatch):
    import json
    from backend.app import main

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_ACTIVE_KEY_ID",
        "mac-test-1",
    )

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        json.dumps(
            {
                "mac-test-1":
                    "temporary-test-secret",
            }
        ),
    )

    key_id = (
        main._get_active_report_mac_key_id()
    )

    assert key_id == "mac-test-1"

    assert (
        main._resolve_report_mac_key(
            key_id
        )
        == b"temporary-test-secret"
    )


def test_legacy_paths_preserved():
    source = MAIN.read_text(
        encoding="utf-8",
    )

    assert '@app.post("/sign-report/{report_id}")' in source

    assert (
        '@app.post("/verify-signature/{report_id}")'
        in source
    )


def test_raw_report_columns_no_null_coercion():
    for name in (
        "register_content_mac_for_principal",
        "verify_content_mac_for_principal",
    ):
        source = _function_source(
            REPOSITORY,
            name,
        )

        assert "COALESCE(" not in source
        assert 'or ""' not in source
        assert "public.reports" in source
        assert "public.patients" in source
        assert "public.hospitals" in source


def test_immutable_registration():
    source = _function_source(
        REPOSITORY,
        "register_content_mac_for_principal",
    )

    assert "ON CONFLICT" in source
    assert "DO NOTHING" in source

    assert (
        "ReportContentMacConflictError"
        in source
    )

    assert (
        "UPDATE public.report_content_macs"
        not in source
    )


def test_constant_time_verify():
    source = _function_source(
        REPOSITORY,
        "verify_content_mac_for_principal",
    )

    assert "hmac.compare_digest" in source


def test_keyring_missing_fails_closed(monkeypatch):
    from fastapi import HTTPException
    from backend.app import main

    monkeypatch.delenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        raising=False,
    )

    try:
        main._load_report_mac_keyring()
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError(
            "missing keyring did not fail closed"
        )


def test_keyring_invalid_json_fails_closed(monkeypatch):
    from fastapi import HTTPException
    from backend.app import main

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        "{not-json",
    )

    try:
        main._load_report_mac_keyring()
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError(
            "invalid keyring JSON accepted"
        )


def test_active_key_unknown_fails_closed(monkeypatch):
    import json
    from fastapi import HTTPException
    from backend.app import main

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_ACTIVE_KEY_ID",
        "mac-new",
    )

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        json.dumps(
            {
                "mac-old":
                    "temporary-old-secret",
            }
        ),
    )

    try:
        main._get_active_report_mac_key_id()
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError(
            "unknown active key accepted"
        )


def test_historical_key_resolution(monkeypatch):
    import json
    from backend.app import main

    monkeypatch.setenv(
        "AIHA_REPORT_MAC_KEYS_JSON",
        json.dumps(
            {
                "mac-old": "temporary-old-secret",
                "mac-new": "temporary-new-secret",
            }
        ),
    )

    assert (
        main._resolve_report_mac_key(
            "mac-old"
        )
        == b"temporary-old-secret"
    )

    assert (
        main._resolve_report_mac_key(
            "mac-new"
        )
        == b"temporary-new-secret"
    )


def test_mac_key_id_validation_fails_closed():
    from fastapi import HTTPException
    from backend.app import main

    invalid = (
        "",
        " ",
        "contains space",
        "../bad",
        "x" * 65,
    )

    for key_id in invalid:

        try:
            main._validate_report_mac_key_id(
                key_id
            )
        except HTTPException as exc:
            assert exc.status_code == 503
        else:
            raise AssertionError(
                f"invalid key id accepted: {key_id!r}"
            )


def test_rotation_repository_uses_stored_key_id():
    from pathlib import Path

    source = Path(
        "backend/app/repositories/postgres/"
        "reports_repository.py"
    ).read_text(
        encoding="utf-8"
    )

    assert 'baseline["key_id"]' in source
    assert "baseline_mac_key" in source
    assert "mac_key_resolver(" in source
    assert ":key_id" in source


def test_register_content_mac_has_no_unbound_legacy_mac_key_reference():
    import ast
    import inspect
    import textwrap

    from backend.app.repositories.postgres.reports_repository import (
        PostgresReportsRepository,
    )

    source = textwrap.dedent(
        inspect.getsource(
            PostgresReportsRepository
            .register_content_mac_for_principal
        )
    )

    tree = ast.parse(source)

    legacy_loads = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
        and node.id == "mac_key"
    ]

    assert legacy_loads == []

    assert "mac_key_resolver" in source
    assert "active_mac_key" in source
    assert "baseline_mac_key" in source
