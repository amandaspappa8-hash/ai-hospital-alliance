from .repositories.memory.users_repository import InMemoryUsersRepository
from .repositories.memory.patients_repository import InMemoryPatientsRepository
from .repositories.memory.notes_repository import InMemoryNotesRepository
from .repositories.memory.orders_repository import InMemoryOrdersRepository
from .repositories.memory.appointments_repository import InMemoryAppointmentsRepository
from .repositories.memory.reports_repository import InMemoryReportsRepository
from .repositories.memory.nursing_repository import InMemoryNursingRepository
from .repositories.memory.mar_repository import InMemoryMarRepository
from .repositories.memory.labs_repository import InMemoryLabsRepository
from .repositories.memory.radiology_repository import InMemoryRadiologyRepository
from .repositories.memory.doctor_assignments_repository import InMemoryDoctorAssignmentsRepository

def build_repositories(
    users_store,
    patients_store,
    notes_store,
    orders_store,
    appointments_store=None,
    reports_store=None,
    nursing_vitals_store=None,
    nursing_notes_store=None,
    mar_store=None,
    labs_catalog_store=None,
    lab_orders_store=None,
    radiology_catalog_store=None,
    radiology_orders_store=None,
    doctor_assignments_store=None,
):
    return {
        "users": InMemoryUsersRepository(users_store),
        "patients": InMemoryPatientsRepository(patients_store),
        "notes": InMemoryNotesRepository(notes_store),
        "orders": InMemoryOrdersRepository(orders_store),
        "appointments": InMemoryAppointmentsRepository(appointments_store or []),
        "reports": InMemoryReportsRepository(reports_store or []),
        "nursing": InMemoryNursingRepository(nursing_vitals_store or {}, nursing_notes_store or {}),
        "mar": InMemoryMarRepository(mar_store or {}),
        "labs": InMemoryLabsRepository(labs_catalog_store or {}, lab_orders_store or []),
        "radiology": InMemoryRadiologyRepository(radiology_catalog_store or {}, radiology_orders_store or []),
        "doctor_assignments": InMemoryDoctorAssignmentsRepository(doctor_assignments_store or {}),
    }
