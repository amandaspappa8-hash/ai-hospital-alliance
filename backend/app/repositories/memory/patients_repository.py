from typing import Any


class InMemoryPatientsRepository:
    """Explicit test-only Patient repository.

    Tenant scope is mandatory for visibility. Legacy in-memory records that do
    not carry tenant_id are intentionally invisible through this adapter.
    Patient creation is disabled because memory mode has no trusted canonical
    user -> hospital authority.
    """

    def __init__(self, patients_store: list[dict[str, Any]]):
        self.patients_store = patients_store

    def list_all(
        self,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        del principal_user_id
        return [
            patient
            for patient in self.patients_store
            if str(patient.get("tenant_id", "")) == str(tenant_id)
        ]

    def get_by_id(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        del principal_user_id
        for patient in self.patients_store:
            if (
                patient.get("id") == patient_id
                and str(patient.get("tenant_id", "")) == str(tenant_id)
            ):
                return patient
        return None

    def create(
        self,
        patient: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any]:
        del patient, tenant_id, principal_user_id, ip_address
        raise RuntimeError(
            "Patient create is disabled in explicit memory mode: "
            "canonical hospital authority is unavailable"
        )

    def update(
        self,
        patient_id: str,
        changes: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any] | None:
        del principal_user_id, ip_address

        patient = self.get_by_id(
            patient_id,
            tenant_id,
            principal_user_id=0,
        )

        if patient is None:
            return None

        allowed = {
            "full_name",
            "phone",
            "blood_type",
            "allergies",
            "chronic_conditions",
        }

        for key, value in changes.items():
            if key not in allowed:
                continue

            patient[key] = value

            if key == "full_name":
                patient["name"] = value

        return patient

    def delete(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> bool:
        del principal_user_id, ip_address

        for index, patient in enumerate(self.patients_store):
            if (
                patient.get("id") == patient_id
                and str(patient.get("tenant_id", "")) == str(tenant_id)
            ):
                del self.patients_store[index]
                return True

        return False

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None:
        del patient_id, tenant_id, principal_user_id

        raise PermissionError(
            "Hospital-scoped patient authorization unavailable "
            "for in-memory Patient repository"
        )
