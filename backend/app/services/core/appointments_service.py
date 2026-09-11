class AppointmentsService:
    def __init__(self, appointments_repository):
        self.appointments_repository = appointments_repository

    def list_appointments(
        self,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.appointments_repository,
            "supports_tenant_scope",
            False,
        ):
            return self.appointments_repository.list_all(
                tenant_id,
                principal_user_id,
            )

        return self.appointments_repository.list_all()

    def create_appointment(
        self,
        payload: dict,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.appointments_repository,
            "supports_tenant_scope",
            False,
        ):
            return self.appointments_repository.create(
                payload,
                tenant_id,
                principal_user_id,
            )

        return self.appointments_repository.create(
            payload
        )
