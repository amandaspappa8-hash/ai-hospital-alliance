from .auth_service import AuthService
from .patients_service import PatientsService
from .notes_service import NotesService
from .orders_service import OrdersService
from .appointments_service import AppointmentsService
from .reports_service import ReportsService
from .nursing_service import NursingService
from .mar_service import MarService
from .labs_service import LabsService
from .radiology_service import RadiologyService
from .doctor_assignments_service import DoctorAssignmentsService
from ..ai.clinical_ai_service import ClinicalAIService
from ..ai.drug_intel_service import DrugIntelService


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
        "doctor_assignments": DoctorAssignmentsService(
            repositories["doctor_assignments"]
        ),
        "clinical_ai": ClinicalAIService(repositories["orders"]),
        "drug_intel": DrugIntelService(repositories["mar"]),
    }


# AIHA P4.25 — Unified Dashboard aggregation binding.
#
# The original service registry remains authoritative for existing services.
# This wrapper adds only the dashboard aggregation service.
from .dashboard_aggregation_service import DashboardAggregationService

from backend.app.repositories.dashboard.legacy_operational_metrics import (
    LegacyOperationalMetricsAdapter,
)
from backend.app.repositories.dashboard.subsystem_metrics import (
    ClinicalSafetyMetricsAdapter,
    PersistentEventMetricsAdapter,
    PhysicianReviewMetricsAdapter,
)


_build_services_without_dashboard = build_services


def build_services(repositories):
    services = _build_services_without_dashboard(
        repositories
    )

    services["dashboard"] = (
        DashboardAggregationService(
            patients_service=services[
                "patients"
            ],
            radiology_service=services[
                "radiology"
            ],
            physician_review_adapter=(
                PhysicianReviewMetricsAdapter()
            ),
            persistent_event_adapter=(
                PersistentEventMetricsAdapter()
            ),
            clinical_safety_adapter=(
                ClinicalSafetyMetricsAdapter()
            ),
            legacy_operational_adapter=(
                LegacyOperationalMetricsAdapter()
            ),
        )
    )

    return services
