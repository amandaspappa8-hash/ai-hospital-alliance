from typing import Any
from datetime import datetime


class InMemoryMarRepository:
    def __init__(self, mar_store: dict[str, list[dict[str, Any]]]):
        self.mar_store = mar_store

    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        return list(self.mar_store.get(patient_id, []))

    def create(self, patient_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if patient_id not in self.mar_store:
            self.mar_store[patient_id] = []

        next_id = len(self.mar_store[patient_id]) + 1
        new_item = {
            "id": next_id,
            "medication": payload.get("medication", ""),
            "dose": payload.get("dose", ""),
            "route": payload.get("route", ""),
            "schedule": payload.get("schedule", ""),
            "status": payload.get("status", "Pending"),
            "givenAt": payload.get("givenAt"),
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.mar_store[patient_id].append(new_item)
        return new_item

    def update(self, patient_id: str, item_id: int, payload: dict):
        items = self.mar_store.get(patient_id, [])
        for item in items:
            if int(item.get("id")) != int(item_id):
                continue

            for field in (
                "medication",
                "dose",
                "route",
                "schedule",
            ):
                if field in payload:
                    item[field] = payload[field]

            if payload.get("status") is not None:
                item["status"] = payload["status"]

            if payload.get("givenAt") is not None:
                item["givenAt"] = payload["givenAt"]

            return dict(item)

        return None

    def set_status(self, patient_id: str, item_id: int, payload: dict):
        items = self.mar_store.get(patient_id, [])
        for item in items:
            if int(item.get("id")) != int(item_id):
                continue

            item["status"] = payload.get(
                "status",
                item.get("status"),
            )

            if payload.get("givenAt") is not None:
                item["givenAt"] = payload["givenAt"]

            return dict(item)

        return None

    def set_pharmacy_review(self, patient_id: str, item_id: int, payload: dict):
        items = self.mar_store.get(patient_id, [])
        for item in items:
            if int(item.get("id")) != int(item_id):
                continue

            status = payload.get("status")

            if status is not None:
                item["pharmacyReview"] = status

            return dict(item)

        return None

    def delete(self, patient_id: str, item_id: int) -> bool:
        items = self.mar_store.get(patient_id, [])
        for index, item in enumerate(items):
            if int(item.get("id")) == int(item_id):
                del items[index]
                return True
        return False
