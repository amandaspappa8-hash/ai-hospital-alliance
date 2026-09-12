from typing import Protocol, Any


class RadiologyRepositoryContract(Protocol):
    def get_catalog(self) -> dict[str, Any]: ...

    def list_orders(self) -> list[dict[str, Any]]: ...

    def list_orders_by_patient(self, patient_id: str) -> list[dict[str, Any]]: ...

    def get_study_by_uid(
        self,
        study_uid: str,
    ) -> dict[str, Any] | None: ...

    def create_order(self, payload: dict[str, Any]) -> dict[str, Any]: ...

    def set_result(
        self, order_id: str | int, payload: dict[str, Any]
    ) -> dict[str, Any] | None: ...
