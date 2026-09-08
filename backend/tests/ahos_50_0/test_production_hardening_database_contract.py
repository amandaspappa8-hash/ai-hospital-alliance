import importlib
import os
from pathlib import Path
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


_PHASE50_MODULES = (
    "backend.app.ahos_50_0.production_hardening_platform",
    "backend.app.ahos_50_0.models",
    "backend.app.ahos_50_0.database",
)


@pytest.fixture(scope="module")
def isolated_phase50(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp(
        "phase50_database_contract"
    )

    database_path = temp_dir / "phase50_test.db"
    database_url = f"sqlite:///{database_path}"

    previous_database_url = os.environ.get(
        "DATABASE_URL"
    )

    for module_name in _PHASE50_MODULES:
        sys.modules.pop(module_name, None)

    os.environ["DATABASE_URL"] = database_url

    dbmod = None

    try:
        dbmod = importlib.import_module(
            "backend.app.ahos_50_0.database"
        )

        models = importlib.import_module(
            "backend.app.ahos_50_0.models"
        )

        platform = importlib.import_module(
            "backend.app.ahos_50_0.production_hardening_platform"
        )

        assert dbmod.engine.dialect.name == "sqlite"
        assert models.Base is dbmod.Base

        bound_path = Path(
            dbmod.engine.url.database
        ).resolve()

        assert bound_path == database_path.resolve()
        assert bound_path.name == "phase50_test.db"
        assert bound_path.name != "ahos_runtime.db"

        dbmod.Base.metadata.create_all(
            bind=dbmod.engine
        )

        app = FastAPI()
        app.include_router(platform.router)

        client = TestClient(app)

        yield {
            "client": client,
            "database": dbmod,
            "models": models,
            "platform": platform,
            "database_path": database_path,
        }

    finally:
        if dbmod is not None:
            dbmod.engine.dispose()

        for module_name in _PHASE50_MODULES:
            sys.modules.pop(module_name, None)

        if previous_database_url is None:
            os.environ.pop(
                "DATABASE_URL",
                None,
            )
        else:
            os.environ["DATABASE_URL"] = (
                previous_database_url
            )


def _assert_database_field_matches_engine(
    payload,
    dialect,
):
    assert "database" in payload

    reported = str(
        payload["database"]
    ).strip().lower()

    assert dialect.lower() in reported


def test_health_database_field_matches_bound_engine_dialect(
    isolated_phase50,
):
    client = isolated_phase50["client"]
    dbmod = isolated_phase50["database"]

    response = client.get(
        "/ahos/50.0/production-hardening/health"
    )

    assert response.status_code == 200

    _assert_database_field_matches_engine(
        response.json(),
        dbmod.engine.dialect.name,
    )


def test_dashboard_database_field_matches_bound_engine_dialect(
    isolated_phase50,
):
    client = isolated_phase50["client"]
    dbmod = isolated_phase50["database"]

    response = client.get(
        "/ahos/50.0/production-hardening/dashboard"
    )

    assert response.status_code == 200

    _assert_database_field_matches_engine(
        response.json(),
        dbmod.engine.dialect.name,
    )


def test_dashboard_empty_counts_use_isolated_database(
    isolated_phase50,
):
    client = isolated_phase50["client"]

    response = client.get(
        "/ahos/50.0/production-hardening/dashboard"
    )

    assert response.status_code == 200

    payload = response.json()

    expected_zero_fields = (
        "persistent_hospitals",
        "persistent_users",
        "persistent_clinical_cases",
        "persistent_metrics",
        "persistent_partnerships",
    )

    for field in expected_zero_fields:
        assert payload[field] == 0


def test_phase50_health_and_dashboard_routes_remain_registered(
    isolated_phase50,
):
    platform = isolated_phase50["platform"]

    paths = {
        path
        for route in platform.router.routes
        if (
            path := getattr(
                route,
                "path",
                None,
            )
        )
    }

    assert (
        "/ahos/50.0/production-hardening/health"
        in paths
    )

    assert (
        "/ahos/50.0/production-hardening/dashboard"
        in paths
    )


def test_phase50_db_init_route_is_not_exposed():
    """
    Phase50 schema initialization must not be exposed as an HTTP route.

    This test performs static AST inspection only.
    It does not issue any HTTP request.
    """
    import ast
    from pathlib import Path

    platform_source = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "ahos_50_0"
        / "production_hardening_platform.py"
    )

    tree = ast.parse(
        platform_source.read_text(
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
