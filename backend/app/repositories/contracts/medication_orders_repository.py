from typing import Protocol


class MedicationOrdersRepositoryContract(Protocol):
    """Read boundary for canonical medication-order persistence.

    This contract intentionally exposes only the collection read required
    for the current FHIR MedicationRequest migration slice.

    Clinical writes are deliberately excluded until write authority and
    schema governance are approved separately.
    """

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
        limit: int = 50,
    ) -> list[dict]:
        ...
