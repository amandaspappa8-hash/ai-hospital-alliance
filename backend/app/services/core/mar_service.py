class MarService:
    def __init__(self, mar_repository):
        self.mar_repository = mar_repository

    def list_items(self, patient_id: str):
        return self.mar_repository.list_by_patient(patient_id)

    def create_item(self, patient_id: str, payload: dict):
        return self.mar_repository.create(patient_id, payload)
