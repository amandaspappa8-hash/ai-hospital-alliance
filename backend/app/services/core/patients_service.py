from fastapi import HTTPException

class PatientsService:
    def __init__(self, patients_repository):
        self.patients_repository = patients_repository

    def list_patients(self):
        return self.patients_repository.list_all()

    def get_patient(self, patient_id: str):
        patient = self.patients_repository.get_by_id(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
