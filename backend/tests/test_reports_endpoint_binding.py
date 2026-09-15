from __future__ import annotations

from fastapi.testclient import TestClient

import backend.app.main as main
from backend.app.repositories.memory.reports_repository import (
    InMemoryReportsRepository,
)


client = TestClient(
    main.app,
    raise_server_exceptions=False,
)


def _token(
    *,
    user_id: int = 1,
    tenant_id: str = "TENANT-A",
):
    return main.create_access_token(
        {
            "sub": str(user_id),
            "tenant_id": tenant_id,
        }
    )


def _auth_headers(
    *,
    user_id: int = 1,
    tenant_id: str = "TENANT-A",
):
    return {
        "Authorization":
            "Bearer "
            + _token(
                user_id=user_id,
                tenant_id=tenant_id,
            )
    }


class CapturingScopedRepository:
    def __init__(
        self,
        rows=None,
    ):
        self.rows = rows or []
        self.calls = []

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        self.calls.append(
            {
                "tenant_id":
                    tenant_id,
                "principal_user_id":
                    principal_user_id,
            }
        )

        return list(
            self.rows
        )


class DeniedScopedRepository:
    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        raise PermissionError(
            "tenant mismatch"
        )


class InvalidScopedRepository:
    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        raise ValueError(
            "invalid scope"
        )


def test_reports_anonymous_is_401():
    response = client.get(
        "/reports"
    )

    assert (
        response.status_code
        == 401
    )


def test_reports_unscoped_memory_repository_is_503():
    previous = main.REPOSITORIES.get(
        "reports"
    )

    try:
        main.REPOSITORIES[
            "reports"
        ] = InMemoryReportsRepository(
            []
        )

        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

        assert (
            response.status_code
            == 503
        )

        assert (
            response.json()["detail"]
            == (
                "Canonical scoped Reports "
                "repository unavailable"
            )
        )

    finally:
        main.REPOSITORIES[
            "reports"
        ] = previous


def test_reports_scoped_repository_receives_verified_claims():
    previous = main.REPOSITORIES.get(
        "reports"
    )

    repository = (
        CapturingScopedRepository(
            rows=[
                {
                    "id":
                        "R-1001",
                    "patient_id":
                        "P-1001",
                    "title":
                        "Clinical Report",
                    "type":
                        "Clinical",
                    "status":
                        "Ready",
                    "body":
                        "Body text",
                }
            ]
        )
    )

    try:
        main.REPOSITORIES[
            "reports"
        ] = repository

        response = client.get(
            "/reports",
            headers=_auth_headers(
                user_id=7,
                tenant_id="TENANT-A",
            ),
        )

        assert (
            response.status_code
            == 200
        )

        assert response.json() == [
            {
                "id":
                    "R-1001",
                "patient_id":
                    "P-1001",
                "title":
                    "Clinical Report",
                "type":
                    "Clinical",
                "status":
                    "Ready",
                "body":
                    "Body text",
            }
        ]

        assert repository.calls == [
            {
                "tenant_id":
                    "TENANT-A",
                "principal_user_id":
                    7,
            }
        ]

    finally:
        main.REPOSITORIES[
            "reports"
        ] = previous


def test_reports_permission_error_maps_to_403():
    previous = main.REPOSITORIES.get(
        "reports"
    )

    try:
        main.REPOSITORIES[
            "reports"
        ] = DeniedScopedRepository()

        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

        assert (
            response.status_code
            == 403
        )

        assert (
            response.json()["detail"]
            == "Reports scope denied"
        )

    finally:
        main.REPOSITORIES[
            "reports"
        ] = previous


def test_reports_value_error_maps_to_422():
    previous = main.REPOSITORIES.get(
        "reports"
    )

    try:
        main.REPOSITORIES[
            "reports"
        ] = InvalidScopedRepository()

        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

        assert (
            response.status_code
            == 422
        )

        assert (
            response.json()["detail"]
            == "invalid scope"
        )

    finally:
        main.REPOSITORIES[
            "reports"
        ] = previous


def test_post_reports_endpoint_remains_legacy_and_unmodified():
    import inspect

    route = next(
        route
        for route in main.app.routes
        if getattr(
            route,
            "path",
            None,
        ) == "/reports/{patient_id}"
        and "POST" in (
            getattr(
                route,
                "methods",
                set(),
            )
            or set()
        )
    )

    source = inspect.getsource(
        route.endpoint
    )

    assert (
        "REPORTS.append(report)"
        in source
    )
