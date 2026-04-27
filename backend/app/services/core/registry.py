from .services.core.auth_service import AuthService
from .services.core.patients_service import PatientsService
from .services.core.notes_service import NotesService
from .services.core.orders_service import OrdersService
from .services.core.appointments_service import AppointmentsService
from .services.core.reports_service import ReportsService
from .services.core.nursing_service import NursingService
from .services.core.mar_service import MarService
from .services.core.labs_service import LabsService
from .services.core.radiology_service import RadiologyService
from .services.core.doctor_assignments_service import DoctorAssignmentsService
from .services.ai.clinical_ai_service import ClinicalAIService
from .services.ai.drug_intel_service import DrugIntelService

def build_services(repositories):
    return {
        "auth": AuthService(repositories["users"]),
        "patients": PatientsService(repositories["patients"]),
        "notes": NotesService(repositories["notes"]),
        "orders": OrdersService(repositories["orders"]),
        "appointments": AppointmentsService(repositories["appointments"]),
        "reports": ReportsService(repositories["reports"]),
        "nursing": NursingService(repositories["nursing"]),
        "mar": MarService(repositories["mar"]),
        "labs": LabsService(repositories["labs"]),
        "radiology": RadiologyService(repositories["radiology"]),
        "doctor_assignments": DoctorAssignmentsService(repositories["doctor_assignments"]),
        "clinical_ai": ClinicalAIService(repositories["orders"]),
        "drug_intel": DrugIntelService(repositories["mar"]),
    }
