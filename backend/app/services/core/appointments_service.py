class AppointmentsService:
    def __init__(self, appointments_repository):
        self.appointments_repository = appointments_repository

    def list_appointments(self):
        return self.appointments_repository.list_all()

    def create_appointment(self, payload: dict):
        return self.appointments_repository.create(payload)
