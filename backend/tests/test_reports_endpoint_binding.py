from __future__ import annotations

import ast
from pathlib import Path

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


class CapturingWriteRepository:
    def __init__(self):
        self.calls = []

    def create_for_principal(
        self,
        **kwargs,
    ):
        self.calls.append(
            dict(kwargs)
        )

        return {
            "id":
                "R-0123456789abcdef01",
            "patient_id":
                kwargs["patient_id"],
            "title":
                kwargs["title"],
            "type":
                kwargs["report_type"],
            "summary":
                kwargs["summary"],
            "content":
                kwargs["content"],
            "status":
                kwargs["status"],
        }


class DeniedWriteRepository:
    def create_for_principal(
        self,
        **kwargs,
    ):
        del kwargs

        raise PermissionError(
            "scope denied"
        )


class InvalidWriteRepository:
    def create_for_principal(
        self,
        **kwargs,
    ):
        del kwargs

        raise ValueError(
            "invalid report"
        )


class FailedWriteRepository:
    def create_for_principal(
        self,
        **kwargs,
    ):
        del kwargs

        raise RuntimeError(
            "database unavailable"
        )


def _with_reports_repository(
    repository,
):
    class Scope:
        def __enter__(self):
            self.previous = (
                main.REPOSITORIES.get(
                    "reports"
                )
            )

            main.REPOSITORIES[
                "reports"
            ] = repository

            return repository

        def __exit__(
            self,
            exc_type,
            exc,
            tb,
        ):
            main.REPOSITORIES[
                "reports"
            ] = self.previous

            return False

    return Scope()


def test_reports_anonymous_is_401():
    response = client.get(
        "/reports"
    )

    assert response.status_code == 401


def test_reports_unscoped_memory_repository_is_503():
    with _with_reports_repository(
        InMemoryReportsRepository([])
    ):
        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

    assert response.status_code == 503


def test_reports_scoped_repository_receives_verified_claims():
    repository = (
        CapturingScopedRepository(
            rows=[]
        )
    )

    with _with_reports_repository(
        repository
    ):
        response = client.get(
            "/reports",
            headers=_auth_headers(
                user_id=7,
                tenant_id="TENANT-A",
            ),
        )

    assert response.status_code == 200

    assert repository.calls == [
        {
            "tenant_id": "TENANT-A",
            "principal_user_id": 7,
        }
    ]


def test_post_reports_anonymous_is_401():
    with _with_reports_repository(
        CapturingWriteRepository()
    ):
        response = client.post(
            "/reports/P-1001",
            json={
                "title":
                    "Clinical Report"
            },
        )

    assert response.status_code == 401


def test_post_reports_memory_repository_is_503():
    with _with_reports_repository(
        InMemoryReportsRepository([])
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(),
            json={
                "title":
                    "Clinical Report"
            },
        )

    assert response.status_code == 503

    assert (
        response.json()["detail"]
        == (
            "Canonical writable Reports "
            "repository unavailable"
        )
    )


def test_post_reports_forwards_verified_authority_and_payload():
    repository = (
        CapturingWriteRepository()
    )

    with _with_reports_repository(
        repository
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(
                user_id=7,
                tenant_id="TENANT-A",
            ),
            json={
                "title":
                    "Clinical Report",
                "type":
                    "Clinical",
                "summary":
                    "Summary text",
                "content":
                    "Body text",
                "status":
                    "Ready",
            },
        )

    assert response.status_code == 200

    assert repository.calls == [
        {
            "patient_id":
                "P-1001",
            "tenant_id":
                "TENANT-A",
            "principal_user_id":
                7,
            "title":
                "Clinical Report",
            "report_type":
                "Clinical",
            "summary":
                "Summary text",
            "content":
                "Body text",
            "status":
                "Ready",
        }
    ]

    assert response.json() == {
        "id":
            "R-0123456789abcdef01",
        "patient_id":
            "P-1001",
        "title":
            "Clinical Report",
        "type":
            "Clinical",
        "summary":
            "Summary text",
        "content":
            "Body text",
        "status":
            "Ready",
    }


def test_post_reports_preserves_legacy_defaults():
    repository = (
        CapturingWriteRepository()
    )

    with _with_reports_repository(
        repository
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(
                user_id=7,
                tenant_id="TENANT-A",
            ),
            json={
                "title": "Only title"
            },
        )

    assert response.status_code == 200

    call = repository.calls[0]

    assert (
        call["report_type"]
        == "Clinical Report"
    )

    assert call["summary"] == ""
    assert call["content"] == ""
    assert call["status"] == "Draft"


def test_post_reports_permission_error_maps_to_403():
    with _with_reports_repository(
        DeniedWriteRepository()
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(),
            json={
                "title": "Report"
            },
        )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "Reports scope denied"
    )


def test_post_reports_value_error_maps_to_422():
    with _with_reports_repository(
        InvalidWriteRepository()
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(),
            json={
                "title": "Report"
            },
        )

    assert response.status_code == 422
    assert (
        response.json()["detail"]
        == "invalid report"
    )


def test_post_reports_runtime_failure_maps_to_503():
    with _with_reports_repository(
        FailedWriteRepository()
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(),
            json={
                "title": "Report"
            },
        )

    assert response.status_code == 503


def test_post_reports_does_not_append_process_memory():
    repository = (
        CapturingWriteRepository()
    )

    before = list(
        main.REPORTS
    )

    with _with_reports_repository(
        repository
    ):
        response = client.post(
            "/reports/P-1001",
            headers=_auth_headers(),
            json={
                "title": "Report"
            },
        )

    assert response.status_code == 200

    assert main.REPORTS == before


def test_post_reports_source_has_no_reports_append():
    path = Path(
        "backend/app/main.py"
    )

    text = path.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(text)

    found = []

    for node in tree.body:
        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            continue

        if node.name != "create_report":
            continue

        segment = (
            ast.get_source_segment(
                text,
                node,
            )
            or ""
        )

        found.append(segment)

    assert len(found) == 1

    source = found[0]

    assert "REPORTS.append" not in source
    assert "len(REPORTS)" not in source
    assert "create_for_principal" in source
    assert "get_verified_principal_tenant" in source


def test_post_reports_openapi_contract_preserved():
    schema = main.app.openapi()

    post = schema[
        "paths"
    ][
        "/reports/{patient_id}"
    ][
        "post"
    ]

    assert (
        post["operationId"]
        == "create_report_reports__patient_id__post"
    )

    assert (
        post["requestBody"]
        ["content"]
        ["application/json"]
        ["schema"]
        ["$ref"]
        == (
            "#/components/schemas/"
            "ReportCreateRequest"
        )
    )

    assert "200" in post["responses"]
    assert "422" in post["responses"]


class DeniedReadRepository:
    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        del tenant_id
        del principal_user_id

        raise PermissionError(
            "scope denied"
        )


class InvalidReadRepository:
    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        del tenant_id
        del principal_user_id

        raise ValueError(
            "invalid scope"
        )


def test_reports_permission_error_maps_to_403():
    with _with_reports_repository(
        DeniedReadRepository()
    ):
        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == "Reports scope denied"
    )


def test_reports_value_error_maps_to_422():
    with _with_reports_repository(
        InvalidReadRepository()
    ):
        response = client.get(
            "/reports",
            headers=_auth_headers(),
        )

    assert response.status_code == 422

    assert (
        response.json()["detail"]
        == "invalid scope"
    )
