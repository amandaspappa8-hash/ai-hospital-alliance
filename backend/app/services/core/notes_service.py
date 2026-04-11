class NotesService:
    def __init__(self, notes_repository):
        self.notes_repository = notes_repository

    def list_notes(self, patient_id: str):
        return self.notes_repository.list_by_patient(patient_id)

    def create_note(self, patient_id: str, text: str):
        return self.notes_repository.create(patient_id, text)
