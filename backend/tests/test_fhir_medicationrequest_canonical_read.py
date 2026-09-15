import pytest
from fastapi import HTTPException

import backend.app.main as main


class FakeMedicationOrdersRepository:
    def __init__(
        self,
        rows=None,
        error=None,
    ):
        self.rows = rows or []
        self.error = error
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
                "principal_user_id": principal_user_id,
                "limit": limit,
            }
        )

        if self.error is not None:
            raise self.error

        return list(self.rows)


class FakeState:
    auth_payload = {
        "sub": "7",
        "tenant_id": "tenant-1",
    }


class FakeRequest:
    state = FakeState()


def _row():
    return {
        "id": 10,
        "patient_id": "P-001",
        "drug_name": "Example Drug",
        "generic_name": "Example Generic",
        "dose": "10 mg",
        "route": "PO",
        "frequency": "daily",
        "duration_days": 7,
        "quantity": 7,
        "is_active": True,
        "created_at": None,
    }


def test_repository_disabled_fails_closed_503(
    monkeypatch,
):
    monkeypatch.setitem(
        main.REPOSITORIES,
        "medication_orders",
        None,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_medication_requests(
            request=FakeRequest(),
            current_user={"sub": "7"},
        )

    assert exc.value.status_code == 503


def test_canonical_repository_receives_verified_scope(
    monkeypatch,
):
    repository = FakeMedicationOrdersRepository(
        rows=[_row()]
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "medication_orders",
        repository,
    )

    result = main.fhir_medication_requests(
        request=FakeRequest(),
        current_user={"sub": "7"},
    )

    assert repository.calls == [
        {
            "tenant_id": "tenant-1",
            "principal_user_id": 7,
            "limit": 50,
        }
    ]

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "searchset"

    assert (
        result["entry"][0]["resource"]
        ["resourceType"]
        == "MedicationRequest"
    )

    assert (
        result["entry"][0]["resource"]["subject"]
        ["reference"]
        == "Patient/P-001"
    )


def test_repository_permission_error_maps_to_403(
    monkeypatch,
):
    repository = FakeMedicationOrdersRepository(
        error=PermissionError(
            "scope denied"
        )
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "medication_orders",
        repository,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_medication_requests(
            request=FakeRequest(),
            current_user={"sub": "7"},
        )

    assert exc.value.status_code == 403


def test_invalid_verified_principal_remains_401(
    monkeypatch,
):
    class InvalidState:
        auth_payload = {
            "sub": "not-int",
            "tenant_id": "tenant-1",
        }

    class InvalidRequest:
        state = InvalidState()

    repository = FakeMedicationOrdersRepository(
        rows=[_row()]
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "medication_orders",
        repository,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_medication_requests(
            request=InvalidRequest(),
            current_user={},
        )

    assert exc.value.status_code == 401
    assert repository.calls == []
