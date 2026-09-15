from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

import backend.app.main as main


EXPECTED_KEYS = {
    "id",
    "user_id",
    "action",
    "resource",
    "success",
    "timestamp",
    "ip",
}


class CaptureRepository:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.calls = []

    def list_for_principal(
        self,
        *,
        tenant_id,
        principal_user_id,
        limit,
    ):
        self.calls.append(
            {
                "tenant_id": tenant_id,
                "principal_user_id":
                    principal_user_id,
                "limit": limit,
            }
        )

        return self.rows


class DenyRepository:
    def list_for_principal(self, **kwargs):
        raise PermissionError(
            "scope denied"
        )


class InvalidRepository:
    def list_for_principal(self, **kwargs):
        raise ValueError(
            "Audit log limit must be between 1 and 100"
        )


@pytest.fixture
def restore_audit_repository():
    original = main.REPOSITORIES.get(
        "audit_logs"
    )

    yield

    main.REPOSITORIES[
        "audit_logs"
    ] = original


def fake_request():
    return SimpleNamespace(
        state=SimpleNamespace()
    )


def test_repository_disabled_returns_503(
    monkeypatch,
    restore_audit_repository,
):
    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            7,
            "TENANT-A",
        ),
    )

    main.REPOSITORIES[
        "audit_logs"
    ] = None

    with pytest.raises(
        HTTPException
    ) as exc:
        main.get_audit_logs(
            request=fake_request(),
            limit=50,
        )

    assert exc.value.status_code == 503
    assert (
        exc.value.detail
        == "Canonical Audit Logs repository unavailable"
    )


def test_scope_denial_returns_403(
    monkeypatch,
    restore_audit_repository,
):
    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            7,
            "TENANT-A",
        ),
    )

    main.REPOSITORIES[
        "audit_logs"
    ] = DenyRepository()

    with pytest.raises(
        HTTPException
    ) as exc:
        main.get_audit_logs(
            request=fake_request(),
            limit=50,
        )

    assert exc.value.status_code == 403
    assert (
        exc.value.detail
        == "Audit log scope denied"
    )


def test_invalid_repository_input_returns_422(
    monkeypatch,
    restore_audit_repository,
):
    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            7,
            "TENANT-A",
        ),
    )

    main.REPOSITORIES[
        "audit_logs"
    ] = InvalidRepository()

    with pytest.raises(
        HTTPException
    ) as exc:
        main.get_audit_logs(
            request=fake_request(),
            limit=101,
        )

    assert exc.value.status_code == 422
    assert (
        "between 1 and 100"
        in exc.value.detail
    )


def test_verified_scope_passed_exactly(
    monkeypatch,
    restore_audit_repository,
):
    rows = [
        {
            "id": 11,
            "user_id": "doctor1",
            "action": "read",
            "resource": "Patient",
            "success": True,
            "timestamp":
                "2026-09-15 10:00:00",
            "ip": "127.0.0.1",
        }
    ]

    repository = CaptureRepository(
        rows=rows
    )

    monkeypatch.setattr(
        main,
        "get_verified_principal_tenant",
        lambda request: (
            7,
            "TENANT-A",
        ),
    )

    main.REPOSITORIES[
        "audit_logs"
    ] = repository

    result = main.get_audit_logs(
        request=fake_request(),
        limit=25,
    )

    assert result == rows

    assert repository.calls == [
        {
            "tenant_id": "TENANT-A",
            "principal_user_id": 7,
            "limit": 25,
        }
    ]

    assert set(result[0].keys()) == EXPECTED_KEYS


def test_anonymous_request_remains_401(
    restore_audit_repository,
):
    client = TestClient(
        main.app,
        raise_server_exceptions=False,
    )

    response = client.get(
        "/audit/logs"
    )

    assert response.status_code == 401
