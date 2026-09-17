import inspect

import pytest

from fastapi import HTTPException

import backend.app.main as main


class FakePatientRepository:
    def __init__(
        self,
        *,
        rows=None,
        row=None,
        error=None,
    ):
        self.rows = (
            list(rows)
            if rows is not None
            else []
        )
        self.row = row
        self.error = error
        self.list_calls = []
        self.get_calls = []

    def list_fhir_for_principal(
        self,
        *,
        tenant_id,
        principal_user_id,
    ):
        self.list_calls.append({
            "tenant_id": tenant_id,
            "principal_user_id": principal_user_id,
        })

        if self.error is not None:
            raise self.error

        return list(self.rows)

    def get_fhir_by_id(
        self,
        patient_id,
        *,
        tenant_id,
        principal_user_id,
    ):
        self.get_calls.append({
            "patient_id": patient_id,
            "tenant_id": tenant_id,
            "principal_user_id": principal_user_id,
        })

        if self.error is not None:
            raise self.error

        return self.row


class FakeState:
    auth_payload = {
        "sub": "7",
        "tenant_id": "tenant-1",
    }


class FakeRequest:
    state = FakeState()


def _row():
    return {
        "id": "P-1001",
        "name": "Jane Doe",
        "gender": "Female",
        "phone": "+46000000000",
        "condition": "Example Condition",
        "status": "Admitted",
        "department_id": 12,
    }


def test_fhir_patient_list_uses_verified_canonical_scope(
    monkeypatch,
):
    repository = FakePatientRepository(
        rows=[_row()],
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        repository,
    )

    result = main.fhir_patients(
        request=FakeRequest(),
        current_user={"sub": "7"},
    )

    assert repository.list_calls == [
        {
            "tenant_id": "tenant-1",
            "principal_user_id": 7,
        }
    ]

    assert result["resourceType"] == "Bundle"
    assert result["type"] == "searchset"
    assert result["total"] == 1

    patient = result["entry"][0]["resource"]

    assert patient["resourceType"] == "Patient"
    assert patient["id"] == "P-1001"
    assert patient["active"] is True
    assert patient["name"][0]["text"] == "Jane Doe"
    assert patient["gender"] == "female"

    department = [
        item
        for item in patient["extension"]
        if item["url"].endswith("/department")
    ]

    assert department == [
        {
            "url": (
                "http://aiha.hospital/"
                "fhir/department"
            ),
            "valueString": "12",
        }
    ]


def test_fhir_patient_get_uses_verified_canonical_scope(
    monkeypatch,
):
    repository = FakePatientRepository(
        row=_row(),
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        repository,
    )

    result = main.fhir_patient(
        patient_id="P-1001",
        request=FakeRequest(),
        current_user={"sub": "7"},
    )

    assert repository.get_calls == [
        {
            "patient_id": "P-1001",
            "tenant_id": "tenant-1",
            "principal_user_id": 7,
        }
    ]

    assert result["resourceType"] == "Patient"
    assert result["id"] == "P-1001"


def test_fhir_patient_missing_maps_to_404(
    monkeypatch,
):
    repository = FakePatientRepository(
        row=None,
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        repository,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_patient(
            patient_id="P-MISSING",
            request=FakeRequest(),
            current_user={"sub": "7"},
        )

    assert exc.value.status_code == 404


def test_fhir_patient_permission_error_maps_to_403(
    monkeypatch,
):
    repository = FakePatientRepository(
        error=PermissionError(
            "scope denied"
        ),
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        repository,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_patients(
            request=FakeRequest(),
            current_user={"sub": "7"},
        )

    assert exc.value.status_code == 403


def test_fhir_patient_repository_capability_missing_503(
    monkeypatch,
):
    class NoFHIRView:
        pass

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        NoFHIRView(),
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_patients(
            request=FakeRequest(),
            current_user={"sub": "7"},
        )

    assert exc.value.status_code == 503


def test_fhir_patient_invalid_verified_principal_is_401(
    monkeypatch,
):
    class InvalidState:
        auth_payload = {
            "sub": "not-int",
            "tenant_id": "tenant-1",
        }

    class InvalidRequest:
        state = InvalidState()

    repository = FakePatientRepository(
        rows=[_row()],
    )

    monkeypatch.setitem(
        main.REPOSITORIES,
        "patients",
        repository,
    )

    with pytest.raises(
        HTTPException
    ) as exc:
        main.fhir_patients(
            request=InvalidRequest(),
            current_user={},
        )

    assert exc.value.status_code == 401
    assert repository.list_calls == []


def test_fhir_patient_routes_no_longer_use_direct_orm():
    list_source = inspect.getsource(
        main.fhir_patients
    )

    get_source = inspect.getsource(
        main.fhir_patient
    )

    for source in (
        list_source,
        get_source,
    ):
        assert "get_verified_principal_tenant" in source
        assert "REPOSITORIES" in source
        assert "Depends(get_current_user)" in source
        assert "Depends(get_db)" not in source
        assert ".query(Patient)" not in source
        assert "from .models import Patient" not in source


def test_fhir_patient_openapi_declares_security():
    schema = main.app.openapi()

    list_operation = (
        schema["paths"]
        ["/fhir/R4/Patient"]
        ["get"]
    )

    get_operation = (
        schema["paths"]
        ["/fhir/R4/Patient/{patient_id}"]
        ["get"]
    )

    assert list_operation.get(
        "security"
    )

    assert get_operation.get(
        "security"
    )


def test_fhir_patient_operation_ids_preserved():
    schema = main.app.openapi()

    assert (
        schema["paths"]
        ["/fhir/R4/Patient"]
        ["get"]
        ["operationId"]
        == "fhir_patients_fhir_R4_Patient_get"
    )

    assert (
        schema["paths"]
        ["/fhir/R4/Patient/{patient_id}"]
        ["get"]
        ["operationId"]
        == "fhir_patient_fhir_R4_Patient__patient_id__get"
    )
