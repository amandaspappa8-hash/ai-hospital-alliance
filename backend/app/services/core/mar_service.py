class MarService:
    def __init__(self, mar_repository):
        self.mar_repository = mar_repository

    def list_items(self, patient_id: str):
        return self.mar_repository.list_by_patient(patient_id)

    def create_item(self, patient_id: str, payload: dict):
        return self.mar_repository.create(patient_id, payload)

    def update_item(self, patient_id: str, item_id: int, payload: dict):
        return self.mar_repository.update(patient_id, item_id, payload)

    def set_status(self, patient_id: str, item_id: int, payload: dict):
        return self.mar_repository.set_status(patient_id, item_id, payload)

    def set_pharmacy_review(self, patient_id: str, item_id: int, payload: dict):
        return self.mar_repository.set_pharmacy_review(patient_id, item_id, payload)

    def delete_item(self, patient_id: str, item_id: int) -> bool:
        return self.mar_repository.delete(patient_id, item_id)

    def resolve_item_id_by_index(self, patient_id: str, index: int):
        items = self.list_items(patient_id)
        if index < 0 or index >= len(items):
            return None
        return items[index].get("id")
