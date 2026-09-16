from __future__ import annotations

import ast
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]

POSTGRES = (
    PROJECT
    / "backend"
    / "app"
    / "repositories"
    / "postgres"
    / "reports_repository.py"
)


def _method_source(name: str) -> str:
    source = POSTGRES.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)

    cls = next(
        node
        for node in tree.body
        if (
            isinstance(node, ast.ClassDef)
            and node.name
            == "PostgresReportsRepository"
        )
    )

    method = next(
        node
        for node in cls.body
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
    )

    return (
        ast.get_source_segment(
            source,
            method,
        )
        or ""
    )


def test_e18b_read_uses_one_transaction():
    method = _method_source(
        "get_verification_for_principal"
    )

    assert method.count(
        "self._engine.begin()"
    ) == 1

    assert (
        "self._engine.connect()"
        not in method
    )


def test_e18b_read_locks_principal_scope():
    method = _method_source(
        "get_verification_for_principal"
    )

    assert method.count(
        "lock_scope=True"
    ) == 1


def test_e18b_read_locks_report_authority():
    method = _method_source(
        "get_verification_for_principal"
    )

    assert method.count(
        "FOR SHARE OF r, p, h"
    ) == 1


def test_e18b_event_read_after_authority_lock():
    method = _method_source(
        "get_verification_for_principal"
    )

    lock_pos = method.index(
        "FOR SHARE OF r, p, h"
    )

    event_sql_pos = method.index(
        "event_statement = text("
    )

    event_read_pos = method.index(
        "row = connection.execute("
    )

    assert lock_pos < event_sql_pos
    assert event_sql_pos < event_read_pos


def test_e18b_read_is_non_mutating():
    method = _method_source(
        "get_verification_for_principal"
    )

    upper = method.upper()

    assert " INSERT " not in upper
    assert " UPDATE " not in upper
    assert " DELETE " not in upper
    assert "FOR UPDATE" not in upper
    assert "SERIALIZABLE" not in upper


def test_e18b_existing_semantics_preserved():
    method = _method_source(
        "get_verification_for_principal"
    )

    assert (
        "verification_type = 'REGISTRATION'"
        in method
    )

    assert "raise PermissionError(" in method
    assert "if row is None:" in method
    assert "return None" in method

    assert (
        "except SQLAlchemyError as exc:"
        in method
    )

    assert (
        '"Canonical Reports database unavailable"'
        in method
    )


def test_e18b_registration_locking_precedent_unchanged():
    method = _method_source(
        "register_verification_for_principal"
    )

    assert method.count(
        "self._engine.begin()"
    ) == 1

    assert "lock_scope=True" in method

    assert (
        "FOR SHARE OF r, p, h"
        in method
    )
