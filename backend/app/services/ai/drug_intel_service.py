class DrugIntelService:
    def __init__(self, mar_repository):
        self.mar_repository = mar_repository

    def _patient_medications(self, patient_id: str) -> list[str]:
        mar_items = self.mar_repository.list_by_patient(patient_id)
        return [item.get("medication", "") for item in mar_items]

    def reconciliation_for_patient(self, patient_id: str, builder):
        medications = self._patient_medications(patient_id)
        return builder(medications)

    def discharge_counseling_for_patient(self, patient_id: str, builder):
        medications = self._patient_medications(patient_id)
        return builder(medications)

    def recommendations_for_patient(self, patient_id: str, age, builder):
        medications = self._patient_medications(patient_id)
        return builder(medications, age)

    def recommendations_from_payload(self, medications, age, builder):
        return builder(medications, age)

    def dose_safety_for_patient(self, patient_id: str, age, analyzer):
        medications = self._patient_medications(patient_id)
        return analyzer(medications, age)

    def dose_safety_from_payload(self, medications, age, analyzer):
        return analyzer(medications, age)

    def interactions_for_patient(self, patient_id: str, analyzer):
        medications = self._patient_medications(patient_id)
        return analyzer(medications)

    def interactions_from_payload(self, medications, analyzer):
        return analyzer(medications)
