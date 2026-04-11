from backend.app.services.core.auth_service import AuthService
from backend.app.services.core.patients_service import PatientsService
from backend.app.services.core.notes_service import NotesService
from backend.app.services.core.orders_service import OrdersService
from backend.app.services.core.appointments_service import AppointmentsService
from backend.app.services.core.reports_service import ReportsService
from backend.app.services.core.nursing_service import NursingService
from backend.app.services.core.mar_service import MarService
from backend.app.services.core.labs_service import LabsService
from backend.app.services.core.radiology_service import RadiologyService
from backend.app.services.core.doctor_assignments_service import DoctorAssignmentsService
from backend.app.services.ai.clinical_ai_service import ClinicalAIService
from backend.app.services.ai.drug_intel_service import DrugIntelService

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
