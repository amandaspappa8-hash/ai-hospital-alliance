from __future__ import annotations

import ast
from pathlib import Path


def test_ahos_52_9_db_init_route_is_not_exposed():
    """
    AHOS 52.9 database initialization must not be exposed over HTTP.

    This is a static source-contract test only. It performs no HTTP request,
    opens no database connection, and executes no SQL.
    """

    source = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "ahos_52_9"
        / "clinical_safety_alert_engine_platform.py"
    )

    tree = ast.parse(
        source.read_text(
            encoding="utf-8",
            errors="replace",
        )
    )

    exposed = []

    for node in tree.body:

        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        for decorator in node.decorator_list:

            if not (
                isinstance(decorator, ast.Call)
                and isinstance(
                    decorator.func,
                    ast.Attribute,
                )
                and decorator.args
            ):
                continue

            try:
                route = ast.literal_eval(
                    decorator.args[0]
                )
            except Exception:
                continue

            if (
                decorator.func.attr.lower() == "post"
                and route == "/db/init"
            ):
                exposed.append(node.name)

    assert exposed == []
