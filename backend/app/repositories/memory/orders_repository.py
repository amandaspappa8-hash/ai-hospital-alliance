from typing import Any

class InMemoryOrdersRepository:
    def __init__(self, orders_store: dict[str, list[dict[str, Any]]]):
        self.orders_store = orders_store

    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        return list(self.orders_store.get(patient_id, []))

    def create(self, patient_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if patient_id not in self.orders_store:
            self.orders_store[patient_id] = []

        next_id = len(self.orders_store[patient_id]) + 1
        new_order = {
            "id": next_id,
            "item": payload.get("item", ""),
            "type": payload.get("type", "General"),
            "priority": payload.get("priority", "routine"),
            "status": payload.get("status", "Pending"),
        }
        self.orders_store[patient_id].append(new_order)
        return new_order
