class NursingService:
    def __init__(self, nursing_repository):
        self.nursing_repository = nursing_repository

    def list_vitals(self, patient_id: str):
        return self.nursing_repository.list_vitals(patient_id)

    def create_vital(self, patient_id: str, payload: dict):
        return self.nursing_repository.create_vital(patient_id, payload)

    def list_notes(self, patient_id: str):
        return self.nursing_repository.list_notes(patient_id)

    def create_note(self, patient_id: str, text: str):
        return self.nursing_repository.create_note(patient_id, text)
