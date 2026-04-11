from typing import Any

class InMemoryLabsRepository:
    def __init__(self, catalog_store: dict[str, Any], orders_store: list[dict[str, Any]]):
        self.catalog_store = catalog_store
        self.orders_store = orders_store

    def get_catalog(self) -> dict[str, Any]:
        return dict(self.catalog_store)

    def list_orders(self) -> list[dict[str, Any]]:
        return list(self.orders_store)

    def list_orders_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        return [order for order in self.orders_store if order.get("patientId") == patient_id]

    def create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        next_id = len(self.orders_store) + 1
        new_order = {
            "id": next_id,
            "patientId": payload.get("patientId", ""),
            "patientName": payload.get("patientName", ""),
            "testName": payload.get("testName", ""),
            "category": payload.get("category", ""),
            "priority": payload.get("priority", "routine"),
            "status": payload.get("status", "Pending"),
            "result": payload.get("result"),
        }
        self.orders_store.append(new_order)
        return new_order

    def set_result(self, order_id: str | int, payload: dict[str, Any]) -> dict[str, Any] | None:
        for order in self.orders_store:
            if str(order.get("id")) == str(order_id):
                order["result"] = payload.get("result", "")
                order["status"] = payload.get("status", "Completed")
                return order
        return None
