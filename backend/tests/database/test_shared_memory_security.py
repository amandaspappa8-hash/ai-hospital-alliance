from __future__ import annotations

import ast
from pathlib import Path


def test_shared_memory_route_is_not_exposed() -> None:
    project_root = Path(__file__).resolve().parents[3]

    source_path = (
        project_root
        / "backend"
        / "app"
        / "database"
        / "ahos_database_api.py"
    )

    source = source_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    tree = ast.parse(source)

    exposed = []

    for node in tree.body:

        if not isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            continue

        for decorator in node.decorator_list:

            if not (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.args
            ):
                continue

            if decorator.func.attr.lower() != "get":
                continue

            try:
                route = ast.literal_eval(
                    decorator.args[0]
                )
            except Exception:
                continue

            if route == "/ahos/db/memory":
                exposed.append(node.name)

    assert exposed == [], (
        "GET /ahos/db/memory must not be exposed "
        f"from the shared production DB API; found {exposed}"
    )
