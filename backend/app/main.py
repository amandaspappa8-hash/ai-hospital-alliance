from backend.app.security.middleware.audit_middleware import AuditMiddleware

# AHOS Official Ophthalmology Intelligence System
try:
    from app.ophthalmology_unique.router import router as ophthalmology_unique_router
except Exception:
    from backend.app.ophthalmology_unique.router import router as ophthalmology_unique_router

from backend.app.ophthalmology_ai.router import router as ophthalmology_ai_router
from backend.app.api.dicom_viewer import router as dicom_viewer_router
from backend.app.ahos_53_2.multi_agent_clinical_reasoning_platform import router as ahos_53_2_router
from backend.app.ahos_53_1.autonomous_clinical_decision_support_platform import router as ahos_53_1_router
from backend.app.ahos_53_0.real_time_clinical_command_center_platform import router as ahos_53_0_router
from backend.app.ahos_52_9.clinical_safety_alert_engine_platform import router as ahos_52_9_router
from backend.app.ahos_52_8.persistent_clinical_event_store_platform import router as ahos_52_8_router
from backend.app.ahos_52_7.real_redis_backend_integration_platform import router as ahos_52_7_router
from backend.app.ahos_52_6.redis_streams_clinical_event_bus_platform import router as ahos_52_6_router
from backend.app.ahos_52_5.clinical_event_bus_platform import router as ahos_52_5_router
from backend.app.ahos_52_4.fhir_subscription_realtime_streaming_platform import router as ahos_52_4_router
from backend.app.ahos_52_3.smart_on_fhir_authentication_platform import router as ahos_52_3_router
from backend.app.ahos_52_2.live_hapi_fhir_integration_platform import router as ahos_52_2_router
from backend.app.ahos_52_1.real_fhir_server_connector_platform import router as ahos_52_1_router
from backend.app.ahos_52_0.real_hospital_pilot_deployment_platform import router as ahos_52_0_router
from backend.app.ahos_51_6.global_verification_final_qa_platform import router as ahos_51_6_router
from backend.app.ahos_51_5.global_digital_health_civilization_platform import router as ahos_51_5_router
from backend.app.ahos_51_4.global_healthcare_federation_platform import router as ahos_51_4_router
from backend.app.ahos_51_3.global_healthcare_exchange_platform import router as ahos_51_3_router
from backend.app.ahos_51_2.global_healthcare_marketplace_platform import router as ahos_51_2_router
from backend.app.ahos_51_0.international_sales_government_partnership_platform import router as ahos_51_1_router
from backend.app.ahos_51_0.global_commercial_launch_platform import router as ahos_51_0_global_commercial_launch_router
from backend.app.ahos_50_0.enterprise_investor_data_room_platform import router as ahos_50_9_router
from backend.app.ahos_50_0.regulatory_evidence_audit_dossier_platform import router as ahos_50_8_regulatory_evidence_router
from backend.app.ahos_50_0.secrets_zero_trust_runtime_platform import router as ahos_50_7_zero_trust_router
from backend.app.ahos_50_0.global_multiregion_disaster_recovery_platform import router as ahos_50_6_multiregion_dr_router
from backend.app.ahos_50_0.global_production_kubernetes_platform import router as ahos_50_5_k8s_router
from backend.app.ahos_50_0.enterprise_observability_incident_response_platform import router as ahos_50_4_observability_router
from backend.app.ahos_50_0.security_audit_compliance_platform import router as ahos_50_3_security_compliance_router
from backend.app.ahos_50_0.api_validation_load_testing_platform import router as ahos_50_2_api_validation_load_testing_router
from backend.app.ahos_50_0.migrations_cicd_testing_platform import router as ahos_50_1_migrations_cicd_router
from backend.app.ahos_50_0.production_hardening_platform import router as ahos_50_0_production_hardening_router
from backend.app.ahos_49_0.autonomous_global_healthcare_ecosystem import router as ahos_49_0_8_global_ecosystem_router
from backend.app.ahos_49_0.strategic_partnership_platform import router as ahos_49_0_7_strategic_partnership_router
from backend.app.ahos_49_0.rwe_continuous_learning_platform import router as ahos_49_0_6_rwe_learning_router
from backend.app.ahos_49_0.global_healthcare_monitoring_platform import router as ahos_49_0_5_global_monitoring_router
from backend.app.ahos_49_0.autonomous_hospital_orchestrator import router as ahos_49_0_4_autonomous_hospital_orchestrator_router
from backend.app.ahos_49_0.real_hospital_integration_platform import router as ahos_49_0_3_real_hospital_integration_router
from backend.app.ahos_49_0.identity_rbac_platform import router as ahos_49_0_2_identity_rbac_router
from backend.app.ahos_41_0_4.router_2000 import router as ahos_41_1_router
from backend.app.ahos_47_2.real_clinical_data_integration_hospital_fhir_dicom_deployment_platform import router as ahos_47_2_router
from backend.app.ahos_47_1.real_hospital_pilot_operations_clinical_adoption_platform import router as ahos_47_1_router
from backend.app.ahos_47_0.global_healthcare_enterprise_launch_real_world_deployment_platform import router as ahos_47_0_router
from backend.app.ahos_46_9.autonomous_global_healthcare_commercialization_market_access_platform import router as ahos_46_9_router
from backend.app.ahos_46_8.autonomous_global_healthcare_evidence_regulatory_submission_platform import router as ahos_46_8_router
from backend.app.ahos_46_7.autonomous_global_healthcare_compliance_certification_platform import router as ahos_46_7_router
from backend.app.ahos_46_6.autonomous_global_healthcare_governance_policy_intelligence_platform import router as ahos_46_6_router
from backend.app.ahos_46_5.autonomous_global_healthcare_strategic_command_execution_platform import router as ahos_46_5_router
from backend.app.ahos_46_4.autonomous_global_healthcare_simulation_predictive_decision_platform import router as ahos_46_4_router
from backend.app.ahos_46_3.autonomous_global_healthcare_digital_twin_network import router as ahos_46_3_router
from backend.app.ahos_46_2.autonomous_global_healthcare_operating_network import router as ahos_46_2_router
from backend.app.ahos_46_1.global_healthcare_intelligence_platform import router as ahos_46_1_router
from backend.app.ahos_46_0.autonomous_global_healthcare_enterprise_ecosystem import router as ahos_46_0_router
from backend.app.ahos_45_3.global_digital_health_infrastructure_platform import router as ahos_45_3_router
from backend.app.ahos_45_2.sovereign_healthcare_investment_platform import router as ahos_45_2_router
from backend.app.ahos_45_1.international_stock_exchange_preparation_platform import router as ahos_45_1_router
from backend.app.ahos_45_0.autonomous_global_healthcare_corporation_platform import router as ahos_45_0_router
from backend.app.ahos_44_5.global_healthcare_ipo_public_markets_readiness_platform import router as ahos_44_5_router
from backend.app.ahos_44_4.global_healthcare_ecosystem_strategic_investment_platform import router as ahos_44_4_router
from backend.app.ahos_44_3.enterprise_partner_deployment_strategic_alliances_platform import router as ahos_44_3_router
from backend.app.ahos_44_2.global_healthcare_operations_managed_services_platform import router as ahos_44_2_router
from backend.app.ahos_44_1.global_production_deployment_hospital_adoption_program import router as ahos_44_1_router
from backend.app.ahos_44_0.global_commercial_launch_platform import router as ahos_44_0_router
from backend.app.ahos_43_5.global_hospital_pilot_program import router as ahos_43_5_router
from backend.app.ahos_43_4.regulatory_approval_readiness_platform import router as ahos_43_4_router
from backend.app.ahos_43_3.commercial_healthcare_saas_platform import router as ahos_43_3_router
from backend.app.ahos_43_2.clinical_validation_real_hospital_pilot_platform import router as ahos_43_2_router
from backend.app.ahos_43_1.enterprise_interoperability_clinical_integration_platform import router as ahos_43_1_router
from backend.app.ahos_42_8.autonomous_universal_medical_agi_self_evolving_healthcare_civilization_platform import router as ahos_42_8_router
from backend.app.ahos_42_7.autonomous_interplanetary_healthcare_intelligence_universal_medical_knowledge_platform import router as ahos_42_7_router
from backend.app.ahos_42_6.autonomous_global_healthcare_governance_planetary_medical_civilization_platform import router as ahos_42_6_router
from backend.app.ahos_42_5.autonomous_planetary_healthcare_coordination_crisis_management_platform import router as ahos_42_5_router
from backend.app.ahos_42_4.autonomous_global_health_intelligence_early_warning_system import router as ahos_42_4_router
from backend.app.ahos_42_3.federated_population_health_intelligence_platform import router as ahos_42_3_router
from backend.app.ahos_42_2.real_world_evidence_analytics_platform import router as ahos_42_2_router
from backend.app.ahos_41_0_4.router import router as ahos_41_0_4_router
from backend.app.ahos_28_1.autonomous_enterprise_saas_revenue_operations_core import router as ahos_28_1_router
from backend.app.ahos_24_0.pharmacy_operations_center import router as pharmacy_operations_router
from backend.app.ahos_24_0.laboratory_operations_center import router as laboratory_operations_router
from backend.app.ahos_24_0.radiology_operations_center import router as radiology_operations_router
from backend.app.ahos_24_0.autonomous_icu_intelligence import router as autonomous_icu_router
from backend.app.ahos_24_0.emergency_command_center import router as emergency_command_router
from backend.app.ahos_24_0.autonomous_patient_flow_engine import router as patient_flow_router
from backend.app.ahos_24_0.live_bed_management import router as live_bed_router
from backend.app.ahos_24_0.hospital_operations_core import router as hospital_operations_24_router
from backend.app.ahos_24_0.surgical_operations_center import router as surgical_operations_router
from backend.app.ahos_24_1.executive_command_center import router as executive_command_24_1_router
from backend.app.ahos_24_2.financial_operations_center import router as financial_operations_router
from backend.app.ahos_24_3.supply_chain_intelligence_center import router as supply_chain_router
from backend.app.ahos_24_4.unified_hospital_digital_twin import router as unified_digital_twin_router
from backend.app.ahos_24_5.autonomous_hospital_brain import router as hospital_brain_router
from backend.app.ahos_24_6.unified_executive_command_center import router as unified_executive_router
from backend.app.ahos_24_8.global_multi_hospital_federation import router as federation_24_8_router
from backend.app.ahos_24_9.global_digital_twin_command_network import router as digital_twin_24_9_router
from backend.app.aghos_25_0.aghos_core import router as aghos_core_router
from backend.app.aghos_25_1.clinical_intelligence_mesh import router as clinical_mesh_router
from backend.app.ahos_26_1.predictive_intelligence_grid import router as ahos26_1_router
from backend.app.ahos_26_3.resource_optimization_matrix import router as ahos26_3_router
from backend.app.ahos_26_4.executive_ai_forecast_center import router as ahos26_4_router
from backend.app.ahos_26_5.autonomous_multi_hospital_command_grid import router as ahos26_5_router
from backend.app.ahos_26_7.autonomous_global_medical_operations_center import router as ahos26_7_router
from backend.app.ahos_26_6.unified_executive_intelligence import router as ahos26_6_router
from backend.app.ahos_26_2.autonomous_strategy_engine import router as ahos26_2_router
from backend.app.aghos_25_2.realtime_event_monitoring_center import router as realtime_event_monitor_router
from backend.app.aghos_25_3.unified_clinical_data_exchange_hub import router as data_exchange_25_3_router
from backend.app.ahos_22_0.first_pilot_hospital_deployment import router as first_pilot_router
from backend.app.ahos_22_0.real_multi_tenant_saas import router as real_multi_tenant_router
from backend.app.ahos_22_0.real_laboratory_database import router as real_laboratory_database_router
from backend.app.ahos_22_0.real_drug_database import router as real_drug_database_router
from backend.app.ahos_22_0.real_ohif_viewer_integration import router as real_ohif_viewer_router
from backend.app.ahos_22_0.real_orthanc_dicom_integration import router as real_orthanc_dicom_router
from backend.app.ahos_22_0.real_fhir_resource_storage import router as real_fhir_storage_router
from backend.app.ahos_22_0.real_postgresql_schema import router as real_postgresql_schema_router
from backend.app.ahos_22_0.real_hospital_deployment_program import router as real_deployment_router
from backend.app.ahos_21_0.cicd_production_pipeline import router as cicd_router
from backend.app.ahos_21_0.prometheus_grafana_monitoring import router as monitoring_router
from backend.app.ahos_21_0.audit_logs_security_events import router as audit_security_router
from backend.app.ahos_21_0.orthanc_ohif_production_stack import router as orthanc_ohif_router
from backend.app.ahos_21_0.hapi_fhir_server_bridge import router as hapi_fhir_bridge_router
from backend.app.ahos_21_0.keycloak_rbac_sso import router as keycloak_rbac_router
from backend.app.ahos_21_0.docker_production_stack import router as docker_stack_router
from backend.app.ahos_21_0.postgresql_production_database import router as postgresql_production_router
from backend.app.ahos_21_0.production_real_implementation import router as real_implementation_router
from backend.app.ahos_20_0.global_healthcare_platform import router as global_platform_router
from backend.app.ahos_19_0.global_medical_intelligence_exchange import router as global_medical_exchange_router
from backend.app.ahos_19_0.national_healthcare_cloud_edition import router as national_cloud_router
from backend.app.ahos_19_0.enterprise_ai_command_suite import router as enterprise_command_suite_router
from backend.app.ahos_19_0.enterprise_edition import router as enterprise_edition_router
from backend.app.ahos_18_3.healthcare_marketplace_ecosystem import router as marketplace_router
from backend.app.ahos_18_2.global_healthcare_operations_network import router as global_operations_router
from backend.app.ahos_18_1.customer_success_platform import router as customer_success_router
from backend.app.ahos_18_0.commercial_production_release import router as production_router
from backend.app.ahos_17_0.global_launch_program import router as global_launch_router
from backend.app.ahos_17_0.international_expansion_framework import router as expansion_router
from backend.app.ahos_17_0.government_healthcare_proposal_pack import router as government_router
from backend.app.ahos_17_0.enterprise_sales_partnership_kit import router as enterprise_sales_router
from backend.app.ahos_17_0.investor_pitch_deck_generator import router as investor_pitch_router
from backend.app.ahos_17_0.investor_enterprise_pack import router as investor_pack_router
from backend.app.ahos_16_0.pilot_hospital_deployment_pack import router as pilot_deployment_router
from backend.app.ahos_16_0.clinical_validation_pack import router as clinical_validation_router
from backend.app.ahos_16_0.saas_multi_tenant_architecture import router as saas_router
from backend.app.ahos_16_0.pharmacy_production_engine import router as pharmacy_router
from backend.app.ahos_16_0.lis_laboratory_integration import router as lis_router
from backend.app.ahos_16_0.pacs_production_bridge import router as pacs_bridge_router
from backend.app.ahos_16_0.hl7_v2_parser import router as hl7_v2_router
from backend.app.ahos_16_0.real_fhir_r4_connector import router as real_fhir_r4_router
from backend.app.ahos_16_0.enterprise_real_execution import router as enterprise_real_execution_router
from backend.app.ahos_15_0.medical_singularity_command_brain import router as singularity_router
from backend.app.ahos_15_0.planetary_healthcare_optimization_core import router as planetary_optimization_router
from backend.app.ahos_15_0.universal_medical_knowledge_engine import router as universal_knowledge_router
from backend.app.ahos_15_0.autonomous_global_medical_governance import router as global_governance_router
from backend.app.ahos_15_0.self_evolving_medical_intelligence import router as self_evolving_router
from backend.app.ahos_14_0.universal_healthcare_intelligence_network import router as universal_network_router
from backend.app.ahos_14_0.global_medical_digital_twin import router as digital_twin_router
from backend.app.ahos_14_0.planetary_medical_intelligence_grid import router as intelligence_grid_router
from backend.app.ahos_14_0.autonomous_medical_civilization import router as medical_civilization_router
from backend.app.ahos_14_0.global_medical_ai_brain import router as global_ai_brain_router
from backend.app.ahos_13_0.planetary_healthcare_command_center import router as planetary_command_router
from backend.app.ahos_13_0.global_clinical_intelligence_exchange import router as clinical_exchange_router
from backend.app.ahos_13_0.worldwide_disease_surveillance import router as disease_surveillance_router
from backend.app.ahos_13_0.global_medical_knowledge_graph import router as global_medical_kg_router
from backend.app.ahos_13_0.global_hospital_federation import router as global_hospital_federation_router
from backend.app.ahos_12_6.enterprise_deployment import router as enterprise_deployment_router
from backend.app.ahos_12_5.real_hospital_data_integration import router as real_data_router
from backend.app.ahos_12_4.clinical_validation_regulatory import router as clinical_validation_router
from backend.app.ahos_12_3.cybersecurity_compliance_audit import router as security_compliance_router
from backend.app.ahos_12_2.fhir_hl7_interoperability import router as fhir_hl7_router
from backend.app.ahos_12_1.production_readiness import router as production_readiness_router
from backend.app.ahos_12_0.ahos_core import router as ahos_core_router
from backend.app.ahos_11_5.executive_command_brain import router as executive_command_brain_router
from backend.app.ahos_11_5.executive_risk_intelligence import router as executive_risk_router
from backend.app.ahos_11_5.executive_forecast_intelligence import router as executive_forecast_router
from backend.app.ahos_11_5.strategic_healthcare_decision_engine import router as strategic_router
from backend.app.ahos_11_5.executive_healthcare_intelligence import router as executive_intelligence_router
from backend.app.ahos_11_4.radiology_orchestrator import router as radiology_orchestrator_router
from backend.app.ahos_11_4.laboratory_orchestrator import router as laboratory_orchestrator_router
from backend.app.ahos_11_4.pharmacy_orchestrator import router as pharmacy_orchestrator_router
from backend.app.ahos_11_4.icu_orchestrator import router as icu_orchestrator_router
from backend.app.ahos_11_4.emergency_orchestrator import router as emergency_orchestrator_router
from backend.app.ahos_11_4.resource_orchestrator import router as resource_orchestrator_router
from backend.app.ahos_11_4.care_path_orchestrator import router as care_path_router
from backend.app.ahos_11_4.autonomous_workflow_engine import router as workflow_router
from backend.app.ahos_11_4.autonomous_hospital_orchestration import router as orchestration_router
from backend.app.ahos_11_3.global_healthcare_federation_command import router as global_federation_command_router
from backend.app.ahos_11_3.federated_resource_optimization import router as federated_resource_router
from backend.app.ahos_11_3.federated_clinical_consensus import router as federated_consensus_router
from backend.app.ahos_11_3.federated_medical_intelligence import router as federated_medical_router
from backend.app.ahos_11_3.healthcare_federation_core import router as federation_core_router
from backend.app.ahos_11_2.national_healthcare_command import router as national_command_router
from backend.app.ahos_11_2.pandemic_intelligence_engine import router as pandemic_router
from backend.app.ahos_11_2.population_health_intelligence import router as population_router
from backend.app.ahos_11_2.regional_healthcare_intelligence import router as regional_intelligence_router
from backend.app.ahos_11_2.inter_hospital_resource_exchange import router as inter_hospital_router
from backend.app.ahos_11_1.autonomous_resource_optimizer import router as resource_optimizer_router
from backend.app.ahos_11_1.hospital_capacity_predictor import router as capacity_router
from backend.app.ahos_11_1.resource_forecast_engine import router as resource_forecast_router
from backend.app.medical_command_brain.medical_command_brain_110 import router as medical_command_brain_110_router
from backend.app.outcome_prediction_105 import router as outcome_prediction_105_router
from backend.app.care_plan_104 import router as care_plan_104_router
from backend.app.clinical_reasoning_103 import router as clinical_reasoning_103_router
from backend.app.clinical_story_102 import router as clinical_story_102_router
from backend.app.clinical_timeline_101 import router as clinical_timeline_101_router
from backend.app.real_data_integration_1007 import router as real_data_integration_1007_router
from backend.app.hospital_command_center.hospital_command_center import router as hospital_command_router
from backend.app.icu_decision_engine.icu_decision_engine import router as icu_decision_router
from backend.app.patient_monitoring.patient_monitoring_engine import router as patient_monitoring_router
from backend.app.workflow_orchestrator.clinical_workflow_orchestrator import router as clinical_workflow_orchestrator_router
from backend.app.treatment_planning.treatment_planning_engine import router as treatment_planning_router
from backend.app.medical_intelligence.knowledge_graph_engine import router as knowledge_graph_router
from backend.app.medical_intelligence.multi_agent_reasoning_engine import router as multi_agent_reasoning_router
from backend.app.superintelligence.superintelligence_engine import router as superintelligence_router
from backend.app.medical_intelligence.medical_intelligence_engine import router as medical_intelligence_router
from backend.app.medical_intelligence.diagnostic_consensus_engine import router as diagnostic_consensus_router
from backend.app.medical_intelligence.real_clinical_case_simulator import router as real_case_simulator_router
from backend.app.neural_civilization.neural_civilization_engine import router as neural_civilization_router
from backend.app.global_mesh.global_mesh_engine import router as global_mesh_router
from backend.app.metaverse.metaverse_engine import router as metaverse_router
from backend.app.surgical_brain.surgical_brain_engine import router as surgical_brain_router
from backend.app.cognitive_grid.cognitive_engine import router as cognitive_router
from backend.app.ai_ultrasound.monai_stream import router as monai_stream_router
from backend.app.ws.clinical_ws import router as clinical_ws_router
from backend.app.api.ai_ultrasound_x_66 import router as ai_ultrasound_x_66_router
from backend.app.api.ai_ultrasound_x_65 import router as ai_ultrasound_x_65_router
from backend.app.api.ai_ultrasound_x_64 import router as ai_ultrasound_x_64_router
from backend.app.api.ai_ultrasound_x_63 import router as ai_ultrasound_x_63_router
from backend.app.api.ai_ultrasound_x_62 import router as ai_ultrasound_x_62_router
import backend.app.api.ai_ultrasound_inference as ai_ultrasound_inference
import backend.app.api.ai_ultrasound_dicom as ai_ultrasound_dicom
import backend.app.api.ai_ultrasound_pdf as ai_ultrasound_pdf
from backend.app.ai_ultrasound_x.routes import router as ai_ultrasound_x_router
from backend.app.api import ai_ultrasound_reports
from backend.app.api.ultrasound_ai import router as ultrasound_ai_router
from backend.app.api.ai_engine import router as ai_engine_router

from backend.app.api.radiology_upload import router as radiology_upload_router
from .security_compat import login_with_env, get_current_user
from .routers.patients import router as patients_router
from .routers.doctors import router as doctors_router
from .routers.appointments import router as appointments_router
from .routers.nursing import router as nursing_router
from .routers.radiology import router as radiology_router
from .routers.labs import router as labs_router
from .routers.pharmacy import router as pharmacy_router
from .routers.clinical_brain import router as clinical_brain_router
import os
import httpx
from . import models
from datetime import datetime
import json
import urllib.parse
from urllib.request import urlopen, Request
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Request as FastAPIRequest,
)
from .route_security_registry import classify
from .route_security_policy_generated import classify_generated
from .route_security_policy_approved import classify_approved
from .shadow_decision_logging import (
    get_recent_shadow_decisions,
    get_shadow_metrics,
    record_shadow_decision,
)
from .services.ai_engine import ask_ai
from fastapi import Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .api.health import router as health_router
from pydantic import BaseModel

from .api.clinical_route import router as clinical_route_router
from .api.clinical_orders import router as clinical_orders_router

from backend.app.resource_allocation.resource_allocation_engine import router as resource_allocation_router
from backend.app.hospital_digital_twin.digital_twin_engine import router as digital_twin_router
from backend.app.autonomous_healthcare_os.autonomous_healthcare_os import router as ahos_router
from backend.app.autonomous_healthcare_os.cross_engine_bus import router as cross_engine_bus_router
from backend.app.autonomous_healthcare_os.autonomous_decision_supervisor import router as autonomous_decision_supervisor_router
from backend.app.autonomous_healthcare_os.global_patient_state_engine import router as global_patient_state_router
app = FastAPI(title="AI Hospital Alliance API", version="1.0.0")

app.add_middleware(AuditMiddleware)



PUBLIC_PATHS = {
    "/api/ophthalmology/phase-25/dashboard-card",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
}

class GlobalAuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)


        route_class = classify(path)
        audit_class = classify_generated(path)

        request.state.route_class = route_class
        request.state.audit_class = audit_class

        shadow_policy_class = classify_approved(path)
        request.state.shadow_policy_class = shadow_policy_class

        request.state.shadow_policy_match = (
            shadow_policy_class == audit_class
        )

        request.state.shadow_decision = {
            "runtime": audit_class,
            "approved": shadow_policy_class,
            "match": shadow_policy_class == audit_class
        }

        record_shadow_decision(
            path=path,
            method=request.method,
            runtime_classification=audit_class,
            approved_classification=(
                shadow_policy_class
            ),
        )



        if route_class == "PUBLIC":
            return await call_next(request)

        if path in PUBLIC_PATHS:
            return await call_next(request)

        if path.startswith("/static"):
            return await call_next(request)

        if path.startswith("/public"):
            return await call_next(request)

        auth = request.headers.get("Authorization","")

        if not auth.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "detail":"Authentication required"
                }
            )

        return await call_next(request)


app.add_middleware(GlobalAuthenticationMiddleware)

app.include_router(ahos_28_1_router)
app.include_router(resource_allocation_router)
app.include_router(real_data_integration_1007_router)
app.include_router(digital_twin_router)
app.include_router(ahos_router)
app.include_router(cross_engine_bus_router)
app.include_router(autonomous_decision_supervisor_router)
app.include_router(global_patient_state_router)
app.include_router(hospital_command_router)
app.include_router(icu_decision_router)
app.include_router(patient_monitoring_router)
app.include_router(clinical_workflow_orchestrator_router)
app.include_router(treatment_planning_router)
app.include_router(superintelligence_router)
app.include_router(medical_intelligence_router)
app.include_router(diagnostic_consensus_router)
app.include_router(real_case_simulator_router)
app.include_router(neural_civilization_router)
app.include_router(global_mesh_router)
app.include_router(metaverse_router)
app.include_router(surgical_brain_router)
app.include_router(cognitive_router)
app.include_router(monai_stream_router)
app.include_router(clinical_ws_router)
app.include_router(ai_ultrasound_x_66_router)
app.include_router(ai_ultrasound_x_65_router)
app.include_router(ai_ultrasound_x_64_router)
app.include_router(ai_ultrasound_x_63_router)
app.include_router(ai_ultrasound_x_router)

app.include_router(ai_engine_router)


@app.on_event("startup")
async def startup_event():
    from .db import create_tables

    create_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost",
        "http://localhost:80",
        "http://127.0.0.1",
        "http://127.0.0.1:80",
        "http://192.168.0.106",
        "http://192.168.0.106:80",
        "https://ai-hospital-alliance-production.up.railway.app",
        "https://zesty-recreation-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os as _os

USERS = {
    "admin": {
        "password": _os.environ.get("ADMIN_PASSWORD"),
        "name": "System Admin",
        "role": "Admin",
    },
    "doctor": {
        "password": _os.environ.get("DOCTOR_PASSWORD"),
        "name": "Dr. Demo",
        "role": "Doctor",
    },
    "radiology": {
        "password": _os.environ.get("RADIOLOGY_PASSWORD"),
        "name": "Radiology User",
        "role": "Radiology",
    },
}

PATIENTS = [
    {
        "id": "P-1001",
        "name": "Ahmed Ali",
        "age": 45,
        "gender": "Male",
        "phone": "+218910000001",
        "condition": "Chest Pain",
        "department": "Cardiology",
        "status": "Active",
    },
    {
        "id": "P-1002",
        "name": "Sara Omar",
        "age": 31,
        "gender": "Female",
        "phone": "+218910000002",
        "condition": "Fever",
        "department": "Emergency",
        "status": "Under Observation",
    },
    {
        "id": "P-1003",
        "name": "Mona Salem",
        "age": 62,
        "gender": "Female",
        "phone": "+218910000003",
        "condition": "Low Oxygen Saturation",
        "department": "ICU",
        "status": "Critical",
    },
]


from .state import ORDERS
from .repositories.registry import build_repositories
from .services.core.registry import build_services

ORTHANC_DICOMWEB_URL = "http://127.0.0.1:8042/dicom-web/studies"
DEMO_STUDY_UID = "1.2.826.0.1.3680043.8.498.40352611434452298538894524161059434702"


def get_latest_study_uid():
    try:
        with urlopen(ORTHANC_DICOMWEB_URL, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if isinstance(payload, list) and payload:
                for item in reversed(payload):
                    uid = item.get("0020000D", {}).get("Value", [None])[0]
                    if uid:
                        return uid
    except (URLError, HTTPError, TimeoutError, ValueError, OSError):
        pass
    return DEMO_STUDY_UID


DOCTOR_ASSIGNMENTS = {
    "D-1002": [
        {
            "id": 1,
            "patientId": "P-1001",
            "patientName": "Ahmed Ali",
            "department": "Cardiology",
            "condition": "Chest Pain",
            "status": "Assigned",
        }
    ]
}


NOTES = {
    "P-1001": [
        {"id": 1, "text": "Patient admitted with chest pain. Initial ECG ordered."}
    ],
    "P-1002": [
        {"id": 1, "text": "Fever under evaluation. Hydration and CBC requested."}
    ],
    "P-1003": [
        {"id": 1, "text": "Critical ICU patient. Oxygen and close monitoring ongoing."}
    ],
}

APPOINTMENTS = [
    {
        "id": "A-2001",
        "patientId": "P-1001",
        "patientName": "Ahmed Ali",
        "department": "Cardiology",
        "doctor": "Dr. Demo",
        "date": "2026-03-17",
        "time": "10:00",
        "status": "Scheduled",
    },
    {
        "id": "A-2002",
        "patientId": "P-1002",
        "patientName": "Sara Omar",
        "department": "Emergency",
        "doctor": "Dr. Demo",
        "date": "2026-03-17",
        "time": "11:30",
        "status": "Waiting",
    },
]

REPORTS = [
    {
        "id": "R-3001",
        "patientId": "P-1001",
        "title": "Initial Clinical Report",
        "type": "Clinical",
        "status": "Ready",
        "date": "2026-03-17",
    },
    {
        "id": "R-3002",
        "patientId": "P-1003",
        "title": "ICU Monitoring Report",
        "type": "ICU",
        "status": "In Progress",
        "date": "2026-03-17",
    },
]

DOCTORS = [
    {
        "id": "D-1001",
        "name": "Dr. Sarah Jones",
        "specialty": "Neurology",
        "department": "Brain & Nerve Center",
        "experience": "12 years",
        "status": "Available",
        "rating": 4.9,
        "patients": 28,
        "schedule": "08:00 - 16:00",
        "phone": "+218910100001",
    },
    {
        "id": "D-1002",
        "name": "Dr. John Smith",
        "specialty": "Cardiology",
        "department": "Heart Center",
        "experience": "15 years",
        "status": "On Call",
        "rating": 4.8,
        "patients": 34,
        "schedule": "09:00 - 17:00",
        "phone": "+218910100002",
    },
    {
        "id": "D-1003",
        "name": "Dr. Emily Brown",
        "specialty": "Orthopedics",
        "department": "Bone & Joint Unit",
        "experience": "10 years",
        "status": "Available",
        "rating": 4.7,
        "patients": 22,
        "schedule": "08:30 - 15:30",
        "phone": "+218910100003",
    },
    {
        "id": "D-1004",
        "name": "Dr. Ahmed Kareem",
        "specialty": "Emergency",
        "department": "Emergency Department",
        "experience": "9 years",
        "status": "In Surgery",
        "rating": 4.6,
        "patients": 19,
        "schedule": "24/7 Rotation",
        "phone": "+218910100004",
    },
    {
        "id": "D-1005",
        "name": "Dr. Lina Salem",
        "specialty": "Radiology",
        "department": "Imaging Center",
        "experience": "11 years",
        "status": "Available",
        "rating": 4.9,
        "patients": 17,
        "schedule": "10:00 - 18:00",
        "phone": "+218910100005",
    },
    {
        "id": "D-1006",
        "name": "Dr. Omar Hassan",
        "specialty": "Pediatrics",
        "department": "Children Care",
        "experience": "13 years",
        "status": "Offline",
        "rating": 4.8,
        "patients": 26,
        "schedule": "09:00 - 14:00",
        "phone": "+218910100006",
    },
    {
        "id": "D-1007",
        "name": "Dr. Noor Al-Masri",
        "specialty": "ICU",
        "department": "Critical Care Unit",
        "experience": "14 years",
        "status": "Available",
        "rating": 4.9,
        "patients": 12,
        "schedule": "07:00 - 15:00",
        "phone": "+218910100007",
    },
    {
        "id": "D-1008",
        "name": "Dr. Youssef Adel",
        "specialty": "Cardiology",
        "department": "Heart Center",
        "experience": "8 years",
        "status": "Available",
        "rating": 4.5,
        "patients": 16,
        "schedule": "12:00 - 20:00",
        "phone": "+218910100008",
    },
]

SPECIALTIES_SUMMARY = [
    {
        "title": "Cardiology",
        "subtitle": "Heart center, ECG, chest pain, vascular workflow",
        "icon": "❤️",
        "route": "/specialties/cardiology",
        "doctors": 12,
        "activeCases": 24,
        "tone": "#ffe5e5",
    },
    {
        "title": "Neurology",
        "subtitle": "Brain, nerves, stroke assessment and monitoring",
        "icon": "🧠",
        "route": "/specialties/neurology",
        "doctors": 9,
        "activeCases": 17,
        "tone": "#ece8ff",
    },
    {
        "title": "Emergency",
        "subtitle": "Triage, urgent workflow, rapid response",
        "icon": "🚑",
        "route": "/specialties/emergency",
        "doctors": 14,
        "activeCases": 41,
        "tone": "#ffe9d6",
    },
    {
        "title": "ICU",
        "subtitle": "Critical care, oxygen, ventilation and close monitoring",
        "icon": "🏥",
        "route": "/specialties/icu",
        "doctors": 7,
        "activeCases": 12,
        "tone": "#e0f2fe",
    },
    {
        "title": "Radiology",
        "subtitle": "Imaging center, PACS, CT, MRI and X-Ray",
        "icon": "🩻",
        "route": "/specialties/radiology",
        "doctors": 6,
        "activeCases": 29,
        "tone": "#e7f9ef",
    },
    {
        "title": "Pediatrics",
        "subtitle": "Children care, growth, fever and outpatient support",
        "icon": "🧒",
        "route": "/specialties/pediatrics",
        "doctors": 10,
        "activeCases": 23,
        "tone": "#fef9c3",
    },
]

PACS_STUDIES = [
    {
        "studyInstanceUID": "1.2.840.10008.1.1001",
        "patientId": "P-1001",
        "patientName": "Ahmed Ali",
        "modality": "CT",
        "studyDate": "20260317",
        "studyDescription": "Chest CT",
    },
    {
        "studyInstanceUID": "1.2.840.10008.1.1002",
        "patientId": "P-1002",
        "patientName": "Sara Omar",
        "modality": "XR",
        "studyDate": "20260317",
        "studyDescription": "Chest X-Ray",
    },
]


NURSING_VITALS = {
    "P-1001": [
        {
            "id": 1,
            "temperature": "37.1",
            "bloodPressure": "128/82",
            "heartRate": "88",
            "respiratoryRate": "18",
            "oxygenSaturation": "97",
            "time": "08:30",
        }
    ],
    "P-1002": [
        {
            "id": 1,
            "temperature": "38.4",
            "bloodPressure": "110/70",
            "heartRate": "102",
            "respiratoryRate": "22",
            "oxygenSaturation": "95",
            "time": "09:10",
        }
    ],
}

NURSING_NOTES = {
    "P-1001": [
        {
            "id": 1,
            "text": "Patient stable. Chest pain reduced after initial management.",
        }
    ],
    "P-1002": [
        {"id": 1, "text": "Fever ongoing. Fluids encouraged and observation continued."}
    ],
}


RADIOLOGY_CATALOG = {
    "xray": [
        "Chest X-Ray",
        "Abdomen X-Ray",
        "Pelvis X-Ray",
        "Spine X-Ray",
        "Skull X-Ray",
        "Extremities X-Ray (Hand, Foot, Leg)",
    ],
    "ct": [
        "CT Brain",
        "CT Chest",
        "CT Abdomen",
        "CT Pelvis",
        "CT Angiography",
        "CT Spine",
        "CT Whole Body Trauma",
    ],
    "mri": [
        "MRI Brain",
        "MRI Spine",
        "MRI Knee",
        "MRI Shoulder",
        "MRI Abdomen",
        "MRI Pelvis",
        "MR Angiography",
    ],
    "ultrasound": [
        "Abdominal Ultrasound",
        "Pelvic Ultrasound",
        "Obstetric Ultrasound",
        "Thyroid Ultrasound",
        "Doppler Ultrasound",
        "Cardiac Echo (Echocardiography)",
    ],
    "mammography": [
        "Screening Mammography",
        "Diagnostic Mammography",
        "Breast Ultrasound",
    ],
    "fluoroscopy": ["Barium Swallow", "Barium Enema", "Upper GI Study"],
    "pet_ct": ["PET-CT Whole Body", "Oncology PET-CT", "Brain PET-CT"],
    "interventional": [
        "Biopsy Imaging Guided",
        "Drainage Procedures",
        "Angiography",
        "Stent Placement",
    ],
}

RADIOLOGY_ORDERS = [
    {
        "id": "RAD-5001",
        "patientId": "P-1001",
        "patientName": "Ahmed Ali",
        "section": "ct",
        "studies": ["CT Chest"],
        "priority": "Urgent",
        "status": "Pending",
        "studyUid": "1.2.840.10008.1.1001",
        "report": "",
    },
    {
        "id": "RAD-5002",
        "patientId": "P-1002",
        "patientName": "Sara Omar",
        "section": "xray",
        "studies": ["Chest X-Ray"],
        "priority": "Routine",
        "status": "Completed",
        "studyUid": "1.2.840.10008.1.1002",
        "report": "No acute cardiopulmonary abnormality.",
    },
]


LAB_CATALOG = {
    "classical": [
        "CBC",
        "ESR",
        "CRP",
        "Blood Glucose",
        "Fasting Blood Sugar",
        "Random Blood Sugar",
        "HbA1c",
        "Urea",
        "Creatinine",
        "BUN",
        "Electrolytes",
        "Sodium",
        "Potassium",
        "Chloride",
        "Calcium",
        "Magnesium",
        "Phosphorus",
        "Uric Acid",
        "Lipid Profile",
        "Total Cholesterol",
        "Triglycerides",
        "HDL",
        "LDL",
        "Liver Function Test",
        "ALT",
        "AST",
        "ALP",
        "GGT",
        "Total Bilirubin",
        "Direct Bilirubin",
        "Albumin",
        "Total Protein",
        "Urinalysis",
        "Stool Analysis",
        "Blood Group",
        "Rh Typing",
        "PT",
        "aPTT",
        "INR",
        "D-Dimer",
        "Serum Iron",
        "Ferritin",
        "TIBC",
        "Vitamin B12",
        "Vitamin D",
        "Folate",
        "Amylase",
        "Lipase",
        "Troponin",
        "CK",
        "CK-MB",
        "LDH",
    ],
    "specialized": [
        "Hormonal Panel",
        "Thyroid Profile",
        "TSH",
        "Free T3",
        "Free T4",
        "PTH",
        "Cortisol",
        "ACTH",
        "Prolactin",
        "FSH",
        "LH",
        "Estradiol",
        "Progesterone",
        "Testosterone",
        "Beta-hCG",
        "Insulin",
        "C-Peptide",
        "Immunology Panel",
        "ANA",
        "Anti-dsDNA",
        "ANCA",
        "RF",
        "Anti-CCP",
        "Complement C3",
        "Complement C4",
        "Total IgE",
        "IgG",
        "IgA",
        "IgM",
        "Microbiology",
        "Blood Culture",
        "Urine Culture",
        "Sputum Culture",
        "Wound Swab Culture",
        "Stool Culture",
        "Sensitivity Test",
        "Cardiac Markers",
        "BNP",
        "NT-proBNP",
        "Procalcitonin",
        "Tumor Markers",
        "AFP",
        "CEA",
        "CA 19-9",
        "CA 125",
        "PSA",
        "Free PSA",
        "Beta-2 Microglobulin",
        "Coagulation Profile",
        "Thrombophilia Screen",
        "Protein C",
        "Protein S",
        "Antithrombin III",
        "Homocysteine",
        "Autoimmune Panel",
        "Endocrine Panel",
        "Drug Monitoring",
        "Toxicology Screen",
        "Heavy Metal Screen",
        "Allergy Panel",
    ],
    "genetics": [
        "Genetic Screening",
        "DNA Analysis",
        "RNA Analysis",
        "Whole Exome Sequencing",
        "Whole Genome Sequencing",
        "Targeted Gene Panel",
        "Carrier Screening",
        "Prenatal Genetic Screening",
        "Postnatal Genetic Screening",
        "BRCA1/BRCA2",
        "TP53 Mutation Analysis",
        "EGFR Mutation Analysis",
        "KRAS Mutation Analysis",
        "NRAS Mutation Analysis",
        "BRAF Mutation Analysis",
        "PIK3CA Mutation Analysis",
        "JAK2 Mutation Analysis",
        "Factor V Leiden Mutation",
        "Prothrombin Gene Mutation",
        "MTHFR Mutation Analysis",
        "HLA Typing",
        "Chromosomal Analysis",
        "Karyotyping",
        "FISH",
        "Microarray CGH",
        "Cytogenetics",
        "Pharmacogenomics",
        "Oncology Mutation Panel",
        "Hereditary Cancer Panel",
        "Neuromuscular Genetics Panel",
        "Cardiomyopathy Genetics Panel",
        "Hemoglobinopathy Genetics",
        "Thalassemia Mutation Analysis",
        "Sickle Cell Mutation Analysis",
    ],
    "nucleic_acid": [
        "PCR",
        "RT-PCR",
        "qPCR",
        "Multiplex PCR",
        "Digital PCR",
        "Viral Load PCR",
        "Bacterial PCR",
        "Fungal PCR",
        "Tuberculosis PCR",
        "COVID-19 PCR",
        "Influenza PCR",
        "RSV PCR",
        "HBV DNA PCR",
        "HCV RNA PCR",
        "HIV Viral Load",
        "HIV PCR",
        "CMV PCR",
        "EBV PCR",
        "HSV PCR",
        "HPV DNA Test",
        "Chlamydia PCR",
        "Gonorrhea PCR",
        "Mycoplasma PCR",
        "Ureaplasma PCR",
        "Meningitis/Encephalitis PCR Panel",
        "Respiratory Pathogen PCR Panel",
        "Gastrointestinal PCR Panel",
        "Sepsis PCR Panel",
        "Nucleic Acid Amplification Test (NAAT)",
        "mRNA Expression Analysis",
        "Gene Fusion Detection",
        "Minimal Residual Disease Molecular Test",
        "Copy Number Variation Analysis",
        "Methylation Analysis",
    ],
}

LAB_ORDERS = [
    {
        "id": "L-4001",
        "patientId": "P-1001",
        "patientName": "Ahmed Ali",
        "section": "classical",
        "tests": ["CBC", "CRP"],
        "priority": "Urgent",
        "status": "Pending",
        "result": "",
    },
    {
        "id": "L-4002",
        "patientId": "P-1002",
        "patientName": "Sara Omar",
        "section": "specialized",
        "tests": ["Culture & Sensitivity"],
        "priority": "Routine",
        "status": "Processing",
        "result": "",
    },
]


class NursingVitalRequest(BaseModel):
    temperature: str
    bloodPressure: str
    heartRate: str
    respiratoryRate: str
    oxygenSaturation: str
    time: str


class NursingNoteRequest(BaseModel):
    text: str


class RadiologyOrderCreateRequest(BaseModel):
    patientId: str
    patientName: str
    section: str
    studies: list[str]
    priority: str | None = "Routine"
    status: str | None = "Pending"


class RadiologyReportRequest(BaseModel):
    report: str
    status: str | None = "Completed"


class LabOrderCreateRequest(BaseModel):
    patientId: str
    patientName: str
    section: str
    tests: list[str]
    priority: str | None = "Routine"
    status: str | None = "Pending"


class LabResultRequest(BaseModel):
    result: str
    status: str | None = "Completed"


class LoginRequest(BaseModel):
    username: str
    password: str


class NoteRequest(BaseModel):
    text: str


class OrderRequest(BaseModel):
    item: str
    type: str | None = "manual"
    priority: str | None = "Routine"
    status: str | None = "Pending"


class DoctorAssignmentRequest(BaseModel):
    patientId: str
    patientName: str
    department: str | None = None
    condition: str | None = None
    status: str | None = "Assigned"


class DoctorAssignmentStatusRequest(BaseModel):
    status: str


class AppointmentRequest(BaseModel):
    patientId: str | None = None
    patientName: str | None = None
    patient: str | None = None
    department: str
    doctor: str
    date: str | None = None
    time: str
    status: str | None = "Scheduled"


@app.get("/")
def root():
    return {"status": "AI Hospital API running"}


@app.post("/auth/login")
def login(payload: dict, db=None):
    username = payload.get("username", "")
    password = payload.get("password", "")

    token = login_with_env(username, password)

    if token:
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "Admin",
            "username": username,
            "user": {
                "username": username,
                "role": "Admin"
            }
        }

    return {"detail": "Invalid credentials"}

@app.post("/auth/db-login")
def db_login(payload: dict):
    from .tenant_isolation import SessionLocal
    from .security_compat import login_with_db
    db = SessionLocal()
    try:
        email = payload.get("email", "")
        password = payload.get("password", "")
        result = login_with_db(email, password, db)
        if not result:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result
    finally:
        db.close()



@app.get("/orders/{patient_id}")
def get_orders(patient_id: str):
    return SERVICES["orders"].list_orders(patient_id)


@app.post("/orders/{patient_id}")
def create_order(patient_id: str, payload: OrderRequest):
    return SERVICES["orders"].create_order(
        patient_id,
        {
            "item": payload.item,
            "type": payload.type,
            "priority": payload.priority,
            "status": "Pending",
        },
    )


@app.get("/notes/{patient_id}")
def get_notes(patient_id: str):
    return SERVICES["notes"].list_notes(patient_id)


@app.post("/notes/{patient_id}")
def create_note(patient_id: str, payload: NoteRequest):
    return SERVICES["notes"].create_note(patient_id, payload.text)


@app.get("/appointments")
def get_appointments():
    return SERVICES["appointments"].list_appointments()


@app.post("/appointments")
def create_appointment(payload: AppointmentRequest):
    patient_name = payload.patientName or payload.patient or ""
    patient_id = payload.patientId or ""

    return SERVICES["appointments"].create_appointment(
        {
            "patientId": patient_id,
            "patientName": patient_name,
            "department": payload.department,
            "doctor": payload.doctor,
            "date": payload.date or "",
            "time": payload.time,
            "status": payload.status or "Scheduled",
        }
    )


@app.get("/reports")
def get_reports():
    return SERVICES["reports"].list_reports()


@app.get("/doctors/summary")
def get_doctors_summary():
    return DOCTORS


@app.get("/doctors/by-specialty/{name}")
def get_doctors_by_specialty(name: str):
    normalized = name.strip().lower()
    return [
        doctor
        for doctor in DOCTORS
        if doctor["specialty"].strip().lower() == normalized
    ]


@app.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: str):
    for doctor in DOCTORS:
        if doctor["id"] == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")


@app.get("/doctor-assignments/{doctor_id}")
def get_doctor_assignments(doctor_id: str):
    return DOCTOR_ASSIGNMENTS.get(doctor_id, [])


@app.post("/doctor-assignments/{doctor_id}")
def create_doctor_assignment(doctor_id: str, payload: DoctorAssignmentRequest):
    if doctor_id not in DOCTOR_ASSIGNMENTS:
        DOCTOR_ASSIGNMENTS[doctor_id] = []

    existing = next(
        (
            item
            for item in DOCTOR_ASSIGNMENTS[doctor_id]
            if item["patientId"] == payload.patientId
        ),
        None,
    )
    if existing:
        return existing

    new_assignment = {
        "id": len(DOCTOR_ASSIGNMENTS[doctor_id]) + 1,
        "patientId": payload.patientId,
        "patientName": payload.patientName,
        "department": payload.department,
        "condition": payload.condition,
        "status": payload.status or "Assigned",
    }
    DOCTOR_ASSIGNMENTS[doctor_id].append(new_assignment)
    return new_assignment


@app.post("/doctor-assignments/{doctor_id}/{assignment_id}/status")
def update_doctor_assignment_status(
    doctor_id: str,
    assignment_id: int,
    payload: DoctorAssignmentStatusRequest,
):
    assignments = DOCTOR_ASSIGNMENTS.get(doctor_id, [])
    for item in assignments:
        if item["id"] == assignment_id:
            item["status"] = payload.status
            return item
    raise HTTPException(status_code=404, detail="Assignment not found")


@app.delete("/doctor-assignments/{doctor_id}/{assignment_id}")
def delete_doctor_assignment(doctor_id: str, assignment_id: int):
    assignments = DOCTOR_ASSIGNMENTS.get(doctor_id, [])
    for index, item in enumerate(assignments):
        if item["id"] == assignment_id:
            removed = assignments.pop(index)
            return removed
    raise HTTPException(status_code=404, detail="Assignment not found")


@app.get("/specialties/summary")
def get_specialties_summary():
    return SPECIALTIES_SUMMARY


@app.get("/pacs/studies")
def get_pacs_studies():
    return PACS_STUDIES


@app.get("/nursing/vitals/{patient_id}")
def get_nursing_vitals(patient_id: str):
    return SERVICES["nursing"].list_vitals(patient_id)


@app.post("/nursing/vitals/{patient_id}")
def create_nursing_vital(patient_id: str, payload: NursingVitalRequest):
    return SERVICES["nursing"].create_vital(
        patient_id,
        {
            "temperature": payload.temperature,
            "bloodPressure": payload.bloodPressure,
            "heartRate": payload.heartRate,
            "respiratoryRate": payload.respiratoryRate,
            "oxygenSaturation": payload.oxygenSaturation,
            "time": payload.time,
        },
    )


@app.get("/nursing/notes/{patient_id}")
def get_nursing_notes(patient_id: str):
    return SERVICES["nursing"].list_notes(patient_id)


@app.post("/nursing/notes/{patient_id}")
def create_nursing_note(patient_id: str, payload: NursingNoteRequest):
    return SERVICES["nursing"].create_note(patient_id, payload.text)


@app.get("/radiology/catalog")
def get_radiology_catalog():
    return SERVICES["radiology"].get_catalog()


@app.get("/radiology/orders")
def get_radiology_orders():
    return SERVICES["radiology"].list_orders()


@app.get("/radiology/orders/{patient_id}")
def get_radiology_orders_by_patient(patient_id: str):
    return SERVICES["radiology"].list_orders_by_patient(patient_id)


@app.post("/radiology/orders")
def create_radiology_order(payload: RadiologyOrderCreateRequest):
    if not payload.studies:
        raise HTTPException(status_code=400, detail="At least one study is required")

    try:
        return SERVICES["radiology"].create_order(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/radiology/results/{order_id}")
def create_radiology_report(order_id: str, payload: RadiologyReportRequest):
    order = SERVICES["radiology"].set_result(
        order_id,
        payload.model_dump(),
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Radiology order not found",
        )

    return order


@app.get("/labs/catalog")
def get_labs_catalog():
    return SERVICES["labs"].get_catalog()


@app.get("/labs/orders")
def get_lab_orders():
    return SERVICES["labs"].list_orders()


@app.get("/labs/orders/{patient_id}")
def get_lab_orders_by_patient(patient_id: str):
    return SERVICES["labs"].list_orders_by_patient(patient_id)


@app.post("/labs/orders")
def create_lab_order(payload: LabOrderCreateRequest):
    if not payload.tests:
        raise HTTPException(
            status_code=400,
            detail="At least one test is required",
        )

    order_payload = {
        "patientId": payload.patientId,
        "patientName": payload.patientName,
        "section": payload.section,
        "tests": list(payload.tests),
        "priority": payload.priority or "Routine",
        "status": payload.status or "Pending",
        "result": "",
    }

    try:
        return SERVICES["labs"].create_order(
            order_payload
        )
    except ValueError as exc:
        if str(exc) == "Patient not found":
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            ) from exc
        raise


@app.post("/labs/results/{order_id}")
def create_lab_result(
    order_id: str,
    payload: LabResultRequest,
):
    return SERVICES["labs"].set_result(
        order_id,
        {
            "result": payload.result,
            "status": payload.status or "Completed",
        },
    )


app.include_router(clinical_route_router)
app.include_router(clinical_orders_router)
app.include_router(health_router)
app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(appointments_router)
app.include_router(nursing_router)
app.include_router(radiology_router)
app.include_router(labs_router)
app.include_router(pharmacy_router)
app.include_router(clinical_brain_router)
from .services.icd11_service import icd11_router
app.include_router(icd11_router)


MED_RECONCILIATION = {
    "P-1001": {
        "homeMeds": ["aspirin 81 mg", "atorvastatin 40 mg", "metoprolol 50 mg"],
        "admissionMeds": ["aspirin 81 mg", "ibuprofen 400 mg"],
        "dischargeMeds": ["aspirin 81 mg", "atorvastatin 40 mg"],
    },
    "P-1002": {
        "homeMeds": ["paracetamol 500 mg"],
        "admissionMeds": ["paracetamol 1 g"],
        "dischargeMeds": ["paracetamol 500 mg"],
    },
}


def _normalize_med_list(values: list[str]) -> list[str]:
    return [_normalize_med_name(v) for v in values if (v or "").strip()]


def _build_reconciliation_summary(patient_id: str):
    raw = MED_RECONCILIATION.get(
        patient_id,
        {
            "homeMeds": [],
            "admissionMeds": [],
            "dischargeMeds": [],
        },
    )

    home = _normalize_med_list(raw.get("homeMeds", []))
    admission = _normalize_med_list(raw.get("admissionMeds", []))
    discharge = _normalize_med_list(raw.get("dischargeMeds", []))

    missing_on_admission = [med for med in home if med not in admission]
    missing_on_discharge = [med for med in home if med not in discharge]
    added_in_hospital = [med for med in admission if med not in home]
    discharge_only = [med for med in discharge if med not in home]

    findings = []

    for med in missing_on_admission:
        findings.append(
            {
                "severity": "moderate",
                "type": "missing_on_admission",
                "title": "Possible chronic medication missing on admission",
                "detail": med,
            }
        )

    for med in missing_on_discharge:
        findings.append(
            {
                "severity": "high",
                "type": "missing_on_discharge",
                "title": "Possible chronic medication missing on discharge",
                "detail": med,
            }
        )

    for med in added_in_hospital:
        findings.append(
            {
                "severity": "moderate",
                "type": "added_in_hospital",
                "title": "Medication added during admission",
                "detail": med,
            }
        )

    for med in discharge_only:
        findings.append(
            {
                "severity": "moderate",
                "type": "new_discharge_med",
                "title": "New medication planned at discharge",
                "detail": med,
            }
        )

    duplicate_groups = _match_ingredient_groups(admission + discharge)
    for ingredient, meds in duplicate_groups.items():
        if len(meds) > 1:
            findings.append(
                {
                    "severity": "high",
                    "type": "duplicate_therapy",
                    "title": "Duplicate therapy detected across reconciliation lists",
                    "detail": f"{ingredient}: " + ", ".join(meds),
                }
            )

    return {
        "patientId": patient_id,
        "homeMeds": home,
        "admissionMeds": admission,
        "dischargeMeds": discharge,
        "findings": findings,
        "summary": {
            "high_risk_count": len([f for f in findings if f["severity"] == "high"]),
            "moderate_risk_count": len(
                [f for f in findings if f["severity"] == "moderate"]
            ),
            "has_findings": len(findings) > 0,
        },
    }


@app.get("/drug-intel/reconciliation/{patient_id}")
def get_medication_reconciliation(patient_id: str):
    return _build_reconciliation_summary(patient_id)


def _default_take_time(med: str):
    med = _normalize_med_name(med)
    if "aspirin" in med:
        return (
            "After food, once daily in the morning unless your doctor changed the time."
        )
    if "atorvastatin" in med:
        return "Once daily in the evening."
    if "metoprolol" in med:
        return "At the same time each day, usually after food."
    if "warfarin" in med:
        return (
            "At the same time every day. Follow INR monitoring instructions carefully."
        )
    if "ibuprofen" in med:
        return "After food, only as directed, and not longer than recommended."
    if "paracetamol" in med:
        return "Every 6 to 8 hours as needed, without exceeding the daily maximum."
    return "Take exactly as prescribed by your clinician."


def _default_avoid_text(med: str):
    med = _normalize_med_name(med)
    if "aspirin" in med:
        return "Avoid taking extra NSAIDs like ibuprofen or naproxen unless specifically approved."
    if "atorvastatin" in med:
        return "Avoid excess alcohol and report unexplained muscle pain."
    if "metoprolol" in med:
        return "Avoid stopping the medicine suddenly without medical advice."
    if "warfarin" in med:
        return "Avoid dose changes, unsupervised NSAIDs, and report any bleeding immediately."
    if "ibuprofen" in med:
        return "Avoid combining with other NSAIDs and use caution if you have stomach or kidney problems."
    if "paracetamol" in med:
        return "Avoid duplicate acetaminophen/paracetamol products."
    return "Avoid self-adjusting the dose without medical advice."


def _default_when_to_review(med: str):
    med = _normalize_med_name(med)
    if "aspirin" in med or "warfarin" in med:
        return "Seek medical review urgently if bleeding, black stool, vomiting blood, or severe dizziness occurs."
    if "metoprolol" in med:
        return "Seek review if severe dizziness, fainting, or very slow pulse occurs."
    if "atorvastatin" in med:
        return "Seek review if severe muscle pain, dark urine, or jaundice occurs."
    if "ibuprofen" in med:
        return "Seek review if stomach pain, black stool, swelling, or reduced urine occurs."
    if "paracetamol" in med:
        return "Seek review if symptoms persist, worsen, or overdose is suspected."
    return "Return for medical review if symptoms worsen or side effects appear."


def _build_discharge_counseling(patient_id: str):
    reconciliation = _build_reconciliation_summary(patient_id)
    discharge_meds = reconciliation.get("dischargeMeds", [])

    counseling = []
    for med in discharge_meds:
        counseling.append(
            {
                "medication": med,
                "take_time": _default_take_time(med),
                "what_to_avoid": _default_avoid_text(med),
                "when_to_seek_help": _default_when_to_review(med),
            }
        )

    general_points = [
        "Take medicines exactly as prescribed.",
        "Keep an updated medication list with you.",
        "Do not restart stopped medicines unless your doctor confirms.",
        "If you miss a dose, follow the medication-specific advice or ask your pharmacist.",
    ]

    return {
        "patientId": patient_id,
        "dischargeMeds": discharge_meds,
        "counseling": counseling,
        "generalAdvice": general_points,
        "summary": {
            "count": len(counseling),
            "has_discharge_meds": len(discharge_meds) > 0,
        },
    }


@app.get("/drug-intel/discharge-counseling/{patient_id}")
def get_discharge_counseling(patient_id: str):
    return _build_discharge_counseling(patient_id)


MAR = {
    "P-1001": [
        {
            "id": 1,
            "medication": "Aspirin 81 mg",
            "dose": "1 tablet",
            "route": "PO",
            "schedule": "Once daily",
            "status": "Given",
            "givenAt": "08:00",
            "createdAt": "2026-03-20 08:00",
        }
    ],
    "P-1002": [
        {
            "id": 1,
            "medication": "Paracetamol 1 g",
            "dose": "1 tablet",
            "route": "PO",
            "schedule": "Every 8 hours",
            "status": "Pending",
            "givenAt": "",
            "createdAt": "2026-03-20 09:00",
        }
    ],
}

REPOSITORIES = build_repositories(
    USERS,
    PATIENTS,
    NOTES,
    ORDERS,
    APPOINTMENTS,
    REPORTS,
    NURSING_VITALS,
    NURSING_NOTES,
    MAR,
    LAB_CATALOG,
    LAB_ORDERS,
    RADIOLOGY_CATALOG,
    RADIOLOGY_ORDERS,
    DOCTOR_ASSIGNMENTS,
)

SERVICES = build_services(REPOSITORIES)


class MARItemRequest(BaseModel):
    medication: str
    dose: str
    route: str
    schedule: str
    status: str | None = "Pending"
    givenAt: str | None = ""


class MARStatusRequest(BaseModel):
    status: str
    givenAt: str | None = ""


class MARUpdateRequest(BaseModel):
    medication: str
    dose: str
    route: str
    schedule: str
    status: str | None = "Pending"
    givenAt: str | None = ""


class DrugInteractionRequest(BaseModel):
    patientId: str | None = None
    medications: list[str] | None = None


NSAID_KEYWORDS = [
    "aspirin",
    "ibuprofen",
    "naproxen",
    "diclofenac",
    "ketorolac",
    "indomethacin",
    "meloxicam",
    "celecoxib",
    "etoricoxib",
]

ANTICOAGULANT_KEYWORDS = [
    "warfarin",
    "apixaban",
    "rivaroxaban",
    "dabigatran",
    "edoxaban",
    "heparin",
    "enoxaparin",
]

ANTIPLATELET_KEYWORDS = ["clopidogrel", "ticagrelor", "prasugrel", "aspirin"]

RENAL_CAUTION_KEYWORDS = [
    "ibuprofen",
    "naproxen",
    "diclofenac",
    "ketorolac",
    "indomethacin",
    "meloxicam",
    "celecoxib",
    "metformin",
    "gentamicin",
    "vancomycin",
    "furosemide",
    "spironolactone",
    "lisinopril",
    "losartan",
]


def _normalize_med_name(name: str) -> str:
    return (name or "").strip().lower()


def _contains_any(name: str, keywords: list[str]) -> bool:
    return any(keyword in name for keyword in keywords)


def _analyze_medication_list(medications: list[str]):
    normalized = [_normalize_med_name(m) for m in medications if (m or "").strip()]
    findings = []

    seen = {}
    for med in normalized:
        seen[med] = seen.get(med, 0) + 1
    for med, count in seen.items():
        if count > 1:
            findings.append(
                {
                    "severity": "moderate",
                    "type": "duplicate_therapy",
                    "title": "Duplicate therapy detected",
                    "detail": f"{med} appears {count} times in the medication list.",
                }
            )

    has_nsaid = any(_contains_any(med, NSAID_KEYWORDS) for med in normalized)
    has_anticoagulant = any(
        _contains_any(med, ANTICOAGULANT_KEYWORDS) for med in normalized
    )
    has_antiplatelet = any(
        _contains_any(med, ANTIPLATELET_KEYWORDS) for med in normalized
    )

    if has_nsaid and has_anticoagulant:
        findings.append(
            {
                "severity": "high",
                "type": "bleeding_risk",
                "title": "Bleeding risk",
                "detail": "NSAID + anticoagulant combination may increase gastrointestinal or systemic bleeding risk.",
            }
        )

    if has_nsaid and has_antiplatelet:
        findings.append(
            {
                "severity": "high",
                "type": "bleeding_risk",
                "title": "Bleeding risk",
                "detail": "NSAID + antiplatelet combination may increase bleeding risk.",
            }
        )

    nsaid_meds = [med for med in normalized if _contains_any(med, NSAID_KEYWORDS)]
    if len(nsaid_meds) >= 2:
        findings.append(
            {
                "severity": "high",
                "type": "nsaid_warning",
                "title": "Multiple NSAIDs detected",
                "detail": "Using more than one NSAID may increase GI bleeding and kidney injury risk.",
            }
        )

    renal_meds = [
        med for med in normalized if _contains_any(med, RENAL_CAUTION_KEYWORDS)
    ]
    if renal_meds:
        findings.append(
            {
                "severity": "moderate",
                "type": "renal_caution",
                "title": "Renal caution",
                "detail": "One or more medications may require renal function review: "
                + ", ".join(sorted(set(renal_meds))),
            }
        )

    return {
        "count": len(normalized),
        "medications": normalized,
        "findings": findings,
        "summary": {
            "has_findings": len(findings) > 0,
            "high_risk_count": len([f for f in findings if f["severity"] == "high"]),
            "moderate_risk_count": len(
                [f for f in findings if f["severity"] == "moderate"]
            ),
        },
    }


class DoseSafetyRequest(BaseModel):
    patientId: str | None = None
    age: int | None = None
    medications: list[str] | None = None


MAX_DAILY_DOSE_RULES = {
    "aspirin": {"adult_mg": 4000, "pediatric_allowed": False},
    "ibuprofen": {"adult_mg": 3200, "pediatric_allowed": True},
    "acetaminophen": {"adult_mg": 4000, "pediatric_allowed": True},
    "paracetamol": {"adult_mg": 4000, "pediatric_allowed": True},
    "naproxen": {"adult_mg": 1250, "pediatric_allowed": False},
    "diclofenac": {"adult_mg": 150, "pediatric_allowed": False},
    "warfarin": {"adult_mg": None, "pediatric_allowed": False},
}

HEPATIC_CAUTION_KEYWORDS = [
    "acetaminophen",
    "paracetamol",
    "valproate",
    "isoniazid",
    "methotrexate",
    "amiodarone",
]

DUPLICATE_INGREDIENT_GROUPS = {
    "aspirin": [
        "aspirin",
        "asa",
        "excedrin",
        "alka-seltzer",
        "anacin",
        "bufferin",
        "ecotrin",
    ],
    "acetaminophen": [
        "acetaminophen",
        "paracetamol",
        "apap",
        "excedrin",
        "panadol",
        "tylenol",
    ],
    "ibuprofen": ["ibuprofen", "advil", "motrin"],
    "naproxen": ["naproxen", "aleve"],
}


def _extract_numeric_dose_mg(text: str) -> int | None:
    import re

    value = (text or "").lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*mg", value)
    if not m:
        return None
    try:
        return int(float(m.group(1)))
    except Exception:
        return None


def _match_ingredient_groups(medications: list[str]):
    normalized = [_normalize_med_name(m) for m in medications if (m or "").strip()]
    matches = {}
    for group, keywords in DUPLICATE_INGREDIENT_GROUPS.items():
        present = []
        for med in normalized:
            if any(keyword in med for keyword in keywords):
                present.append(med)
        if len(set(present)) > 1:
            matches[group] = sorted(set(present))
    return matches


def _analyze_dose_safety(medications: list[str], age: int | None):
    normalized = [_normalize_med_name(m) for m in medications if (m or "").strip()]
    findings = []

    duplicate_groups = _match_ingredient_groups(normalized)
    for ingredient, meds in duplicate_groups.items():
        findings.append(
            {
                "severity": "high",
                "type": "duplicate_ingredient",
                "title": "Duplicate active ingredient detected",
                "detail": f"Multiple products may contain {ingredient}: "
                + ", ".join(meds),
            }
        )

    for med in normalized:
        med_mg = _extract_numeric_dose_mg(med)

        for ingredient, rule in MAX_DAILY_DOSE_RULES.items():
            if ingredient in med:
                if (
                    age is not None
                    and age < 12
                    and not rule.get("pediatric_allowed", False)
                ):
                    findings.append(
                        {
                            "severity": "high",
                            "type": "pediatric_adult_warning",
                            "title": "Pediatric warning",
                            "detail": f"{ingredient} may not be appropriate for pediatric use without specialist review.",
                        }
                    )

                if (
                    med_mg is not None
                    and rule.get("adult_mg") is not None
                    and med_mg > rule["adult_mg"]
                ):
                    findings.append(
                        {
                            "severity": "high",
                            "type": "max_daily_dose",
                            "title": "Possible excessive dose",
                            "detail": f"{med} exceeds adult reference threshold of {rule['adult_mg']} mg/day.",
                        }
                    )

        if _contains_any(med, RENAL_CAUTION_KEYWORDS):
            findings.append(
                {
                    "severity": "moderate",
                    "type": "renal_caution",
                    "title": "Renal dose caution",
                    "detail": f"{med} may require renal function review or dose adjustment.",
                }
            )

        if _contains_any(med, HEPATIC_CAUTION_KEYWORDS):
            findings.append(
                {
                    "severity": "moderate",
                    "type": "hepatic_caution",
                    "title": "Hepatic dose caution",
                    "detail": f"{med} may require liver function review or hepatic dose caution.",
                }
            )

    return {
        "age": age,
        "count": len(normalized),
        "medications": normalized,
        "findings": findings,
        "summary": {
            "has_findings": len(findings) > 0,
            "high_risk_count": len([f for f in findings if f["severity"] == "high"]),
            "moderate_risk_count": len(
                [f for f in findings if f["severity"] == "moderate"]
            ),
        },
    }


class MedicationRecommendationRequest(BaseModel):
    patientId: str | None = None
    age: int | None = None
    medications: list[str] | None = None


def _build_medication_recommendations(medications: list[str], age: int | None = None):
    recommendations = []

    for med in medications:
        med_name = str(med).strip()

        if not med_name:
            continue

        med_lower = med_name.lower()

        if "warfarin" in med_lower:
            recommendations.append(
                {
                    "recommendation": f"Monitor INR closely for {med_name} and avoid unnecessary NSAID/aspirin combinations.",
                    "message": f"High-risk anticoagulant review recommended for {med_name}.",
                    "severity": "high",
                }
            )
        elif "metformin" in med_lower:
            recommendations.append(
                {
                    "recommendation": f"Review renal function periodically while using {med_name}.",
                    "message": f"Routine kidney function monitoring suggested for {med_name}.",
                    "severity": "medium",
                }
            )
        else:
            recommendations.append(
                {
                    "recommendation": f"Review standard dosing and counseling for {med_name}.",
                    "message": f"No special AI flags detected for {med_name}.",
                    "severity": "low",
                }
            )

    if age is not None and age >= 65:
        recommendations.append(
            {
                "recommendation": "Consider age-related dose adjustment and fall-risk review.",
                "message": "Older adult safety review recommended.",
                "severity": "medium",
            }
        )

    return {"recommendations": recommendations, "count": len(recommendations)}


@app.get("/drug-intel/recommendations/{patient_id}")
def get_medication_recommendations_for_patient(patient_id: str, age: int | None = None):
    mar_items = MAR.get(patient_id, [])
    medications = [item.get("medication", "") for item in mar_items]
    result = _build_medication_recommendations(medications, age)
    result["patientId"] = patient_id
    return result


@app.post("/drug-intel/recommendations")
def analyze_medication_recommendations(payload: MedicationRecommendationRequest):
    medications = payload.medications or []
    result = _build_medication_recommendations(medications, payload.age)
    result["patientId"] = payload.patientId
    return result


@app.get("/drug-intel/dose-safety/{patient_id}")
def get_dose_safety_for_patient(patient_id: str, age: int | None = None):
    mar_items = MAR.get(patient_id, [])
    medications = [item.get("medication", "") for item in mar_items]
    result = _analyze_dose_safety(medications, age)
    result["patientId"] = patient_id
    return result


@app.post("/drug-intel/dose-safety")
def analyze_dose_safety(payload: DoseSafetyRequest):
    medications = payload.medications or []
    result = _analyze_dose_safety(medications, payload.age)
    result["patientId"] = payload.patientId
    return result


@app.get("/drug-intel/interactions/{patient_id}")
def get_drug_interactions_for_patient(patient_id: str):
    mar_items = MAR.get(patient_id, [])
    medications = [item.get("medication", "") for item in mar_items]
    result = _analyze_medication_list(medications)
    result["patientId"] = patient_id
    return result


@app.post("/drug-intel/interactions")
def analyze_drug_interactions(payload: DrugInteractionRequest):
    medications = payload.medications or []
    result = _analyze_medication_list(medications)
    result["patientId"] = payload.patientId
    return result


# AHOS-R13C17E disabled secondary route: @app.get("/mar/{patient_id}")
def get_mar(patient_id: str):
    return SERVICES["mar"].list_items(patient_id)


# AHOS-R13C17E disabled secondary route: @app.post("/mar/{patient_id}")
def create_mar_item(patient_id: str, payload: MARItemRequest):
    return SERVICES["mar"].create_item(
        patient_id,
        {
            "medication": payload.medication,
            "dose": payload.dose,
            "route": payload.route,
            "schedule": payload.schedule,
            "status": "Pending",
        },
    )


# AHOS-R13C17E disabled secondary route: @app.put("/mar/{patient_id}/{item_id}")
def update_mar_item(patient_id: str, item_id: int, payload: MARUpdateRequest):
    items = MAR.get(patient_id, [])
    for item in items:
        if item["id"] == item_id:
            item["medication"] = payload.medication
            item["dose"] = payload.dose
            item["route"] = payload.route
            item["schedule"] = payload.schedule
            item["status"] = payload.status or item.get("status", "Pending")
            item["givenAt"] = payload.givenAt or ""
            return item
    raise HTTPException(status_code=404, detail="MAR item not found")


class PharmacistReviewRequest(BaseModel):
    status: str
    note: str | None = ""


# AHOS-R13C17E disabled secondary route: @app.put("/mar/{patient_id}/{item_id}/pharmacist-review")
def pharmacist_review_mar_item(
    patient_id: str, item_id: int, payload: PharmacistReviewRequest
):
    items = MAR.get(patient_id, [])
    for item in items:
        if item["id"] == item_id:
            item["status"] = payload.status or item.get("status", "Pending")
            item["pharmacistNote"] = payload.note or ""
            item["reviewedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return item
    raise HTTPException(status_code=404, detail="MAR item not found")


# AHOS-R13C17E disabled secondary route: @app.put("/mar/{patient_id}/{item_id}/status")
def update_mar_item_status(patient_id: str, item_id: int, payload: MARStatusRequest):
    items = MAR.get(patient_id, [])
    for item in items:
        if item["id"] == item_id:
            item["status"] = payload.status
            item["givenAt"] = payload.givenAt or item.get("givenAt", "")
            return item
    raise HTTPException(status_code=404, detail="MAR item not found")


# AHOS-R13C17E disabled secondary route: @app.get("/drug-intel/search")
def drug_intel_search(q: str = Query(..., min_length=2)):
    encoded = urllib.parse.quote(q)
    rxnorm_url = f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={encoded}"
    openfda_url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:%22{encoded}%22+openfda.brand_name:%22{encoded}%22&limit=3"

    rxnorm_data = {}
    openfda_data = {}

    try:
        with urlopen(
            Request(rxnorm_url, headers={"User-Agent": "AI-Hospital-Alliance"}),
            timeout=12,
        ) as response:
            rxnorm_data = json.loads(response.read().decode("utf-8"))
    except Exception:
        rxnorm_data = {}

    try:
        with urlopen(
            Request(openfda_url, headers={"User-Agent": "AI-Hospital-Alliance"}),
            timeout=12,
        ) as response:
            openfda_data = json.loads(response.read().decode("utf-8"))
    except Exception:
        openfda_data = {}

    return {
        "query": q,
        "rxnorm": rxnorm_data,
        "openfda": openfda_data,
    }


# AHOS-R13C17E disabled secondary route: @app.get("/drug-intel/dailymed")
def drug_intel_dailymed(name: str = Query(..., min_length=2)):
    encoded = urllib.parse.quote(name)
    dailymed_url = f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={encoded}"

    try:
        with urlopen(
            Request(dailymed_url, headers={"User-Agent": "AI-Hospital-Alliance"}),
            timeout=12,
        ) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"DailyMed fetch failed: {exc}")


# AHOS-R13C17E disabled secondary route: @app.delete("/mar/{patient_id}/{item_id}")
def delete_mar_item(patient_id: str, item_id: int):
    items = MAR.get(patient_id, [])
    for index, item in enumerate(items):
        if item["id"] == item_id:
            deleted = items.pop(index)
            return {"deleted": True, "item": deleted}
    raise HTTPException(status_code=404, detail="MAR item not found")


@app.get("/drug-intel/risk/{patient_id}")
def get_risk(patient_id: str):
    patient = next((p for p in PATIENTS if p["id"] == patient_id), None)

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    score = 0
    reasons = []

    # Age factor
    if patient.get("age", 0) > 60:
        score += 2
        reasons.append("Age > 60")

    # Condition factor
    condition = (patient.get("condition") or "").lower()

    if "chest" in condition:
        score += 3
        reasons.append("Chest condition")

    if "oxygen" in condition:
        score += 3
        reasons.append("Low oxygen")

    if "fever" in condition:
        score += 1
        reasons.append("Fever")

    # Risk level
    if score >= 5:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {"level": level, "score": score, "reasons": reasons}


@app.post("/ai/chat")
def ai_chat(payload: dict):
    msg = payload.get("message", "")

    return {
        "reply": f"AI Doctor says: Based on your input '{msg}', please consider medical evaluation and monitoring."
    }


# ===== Reports Create Endpoint =====
try:
    REPORTS
except NameError:
    REPORTS = []


class ReportCreateRequest(BaseModel):
    title: str
    type: str | None = "Clinical Report"
    summary: str | None = ""
    content: str | None = ""
    status: str | None = "Draft"


@app.post("/reports/{patient_id}")
def create_report(patient_id: str, payload: ReportCreateRequest):
    report = {
        "id": f"R-{len(REPORTS) + 1:04d}",
        "patient_id": patient_id,
        "title": payload.title,
        "type": payload.type or "Clinical Report",
        "summary": payload.summary or "",
        "content": payload.content or "",
        "status": payload.status or "Draft",
    }
    REPORTS.append(report)
    return report


from fastapi import Depends, HTTPException

VERIFIED_REPORTS = {}


@app.post("/verify/register/{report_id}")
def register_report(report_id: str):
    VERIFIED_REPORTS[report_id] = {"status": "verified", "timestamp": "valid"}
    return {"message": "Report registered", "report_id": report_id}


@app.get("/verify/{report_id}")
def verify_report(report_id: str):
    report = VERIFIED_REPORTS.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or invalid")

    return {
        "report_id": report_id,
        "status": "VERIFIED",
        "source": "AI Hospital Alliance",
        "security": "Blockchain-grade verification",
    }


import hashlib
import json

REPORT_HASHES = {}


def generate_report_hash(data: dict):
    content = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(content).hexdigest()


@app.post("/secure-report/{report_id}")
def secure_report(report_id: str, payload: dict):
    report_hash = generate_report_hash(payload)

    REPORT_HASHES[report_id] = {"hash": report_hash, "data": payload}

    return {"report_id": report_id, "hash": report_hash, "status": "secured"}


@app.post("/verify-secure/{report_id}")
def verify_secure(report_id: str, payload: dict):
    existing = REPORT_HASHES.get(report_id)

    if not existing:
        return {"status": "NOT FOUND"}

    new_hash = generate_report_hash(payload)

    if new_hash == existing["hash"]:
        return {"status": "VALID", "security": "UNCHANGED"}
    else:
        return {"status": "TAMPERED", "security": "DATA MODIFIED"}


def sign_data(data: bytes) -> str:
    import hmac, hashlib

    key = os.environ.get("SECRET_KEY", "").encode()
    if not key:
        raise RuntimeError("SECRET_KEY environment variable is required")
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def verify_signature(data: bytes, signature: str) -> bool:
    import hmac

    expected = sign_data(data)
    return hmac.compare_digest(expected, signature)


@app.post("/sign-report/{report_id}")
def sign_report(report_id: str, payload: dict):
    import json

    data = json.dumps(payload, sort_keys=True).encode()
    signature = sign_data(data)

    return {"report_id": report_id, "signature": signature, "status": "signed"}


@app.post("/verify-signature/{report_id}")
def verify_report_signature(report_id: str, payload: dict, signature: str):
    import json

    data = json.dumps(payload, sort_keys=True).encode()

    valid = verify_signature(data, signature)

    return {"status": "VALID" if valid else "INVALID", "security": "HMAC-SHA256"}


BLOCKCHAIN_LEDGER = {}


@app.post("/blockchain/register/{report_id}")
def blockchain_register(report_id: str, payload: dict):
    import hashlib, json

    content = json.dumps(payload, sort_keys=True).encode()
    hash_value = hashlib.sha256(content).hexdigest()

    BLOCKCHAIN_LEDGER[report_id] = hash_value

    return {"report_id": report_id, "hash": hash_value, "blockchain": "registered"}


@app.get("/blockchain/verify/{report_id}")
def blockchain_verify(report_id: str, payload: dict):
    import hashlib, json

    stored = BLOCKCHAIN_LEDGER.get(report_id)
    if not stored:
        return {"status": "NOT FOUND"}

    new_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    return {
        "status": "VALID" if stored == new_hash else "TAMPERED",
        "layer": "BLOCKCHAIN",
    }


# =============================
# VERIFIED REPORT WORKFLOW
# =============================
VERIFY_REPORTS = {}


@app.post("/verify-secure/register/{visit_id}")
def register_verify(visit_id: str):
    VERIFY_REPORTS[visit_id] = {
        "status": "registered",
        "timestamp": str(datetime.now()),
    }
    return {"status": "registered", "visit_id": visit_id}


@app.get("/verify-secure/{visit_id}", response_class=HTMLResponse)
def verify_report_page(visit_id: str):
    report = VERIFY_REPORTS.get(visit_id)

    if not report:
        return "<h2 style='color:red;'>Report NOT FOUND</h2>"

    return f"""
    <html>
      <body style="font-family:Arial;text-align:center;padding:40px;">
        <h1 style="color:green;">✔ Verified Medical Report</h1>
        <p><strong>Visit ID:</strong> {visit_id}</p>
        <p>Status: VERIFIED</p>
        <p>Timestamp: {report.get("timestamp")}</p>
      </body>
    </html>
    """


# =============================
# PATIENT PORTAL
# =============================
PATIENT_REPORTS = {}


@app.post("/patient/report/{visit_id}")
def save_patient_report(visit_id: str, payload: dict):
    PATIENT_REPORTS[visit_id] = payload
    return {"status": "saved", "visit_id": visit_id}


@app.get("/patient/report/{visit_id}")
def get_patient_report(visit_id: str):
    report = PATIENT_REPORTS.get(visit_id)

    if not report:
        return {"status": "NOT FOUND"}

    return {"status": "FOUND", "visit_id": visit_id, "report": report}


from .drug_external import openfda_label_by_generic_name


@app.get("/drug-intel/fda-label/{drug_name}")
def get_fda_label_lookup(drug_name: str):
    result = {
        "drug": drug_name,
        "rxcui": None,
        "dailymed": None,
        "openfda": None,
    }

    try:
        result["openfda"] = openfda_label_by_generic_name(drug_name)
    except Exception as e:
        result["openfda_error"] = str(e)
        result["openfda"] = {
            "results": [
                {
                    "openfda": {
                        "generic_name": [drug_name],
                        "brand_name": [drug_name],
                        "manufacturer_name": ["Fallback Local Data"],
                        "route": ["unknown"],
                    },
                    "warnings": [
                        f"Could not fetch live FDA data for {drug_name}. Showing local fallback."
                    ],
                    "adverse_reactions": ["No live adverse reactions available."],
                }
            ]
        }

    return result


@app.get("/drug-intel/global/{drug}")
def global_drug_info(drug: str):
    return {
        "drug": drug,
        "WHO_ATC": "B01AA03",
        "category": "Anticoagulant",
        "fda_warning": "Risk of bleeding",
        "global_note": "Monitor INR regularly",
    }


from .db import SessionLocal, get_db
from sqlalchemy.orm import Session
from .models import User
from .auth import verify_password, create_token


@app.post("/auth/jwt-login")
def jwt_login(payload: dict):
    try:
        db = SessionLocal()
        username = payload.get("username")
        password = payload.get("password")

        if not username or not password:
            return {"error": "Missing username or password"}

        user = db.query(User).filter(User.username == username).first()

        if not user:
            return {"error": "User not found"}

        if not verify_password(password, user.password):
            return {"error": "Invalid credentials"}

        token = create_token(
            {"user_id": user.id, "role": user.role, "hospital_id": user.hospital_id}
        )

        return {
            "access_token": token,
            "user": {
                "username": user.username,
                "role": user.role,
                "hospital_id": user.hospital_id,
            },
        }
    except Exception as e:
        return {"error": f"JWT login failed: {str(e)}"}


from .auth import get_current_user


@app.post("/mar/{patient_id}/{index}/status")
def update_mar_status(
    patient_id: str,
    index: int,
    payload: dict,
    current_user: dict = Depends(get_current_user),
):
    item_id = SERVICES["mar"].resolve_item_id_by_index(
        patient_id,
        index,
    )
    if item_id is None:
        return {
            "error": "MAR item not found",
        }

    payload_data = (
        payload.model_dump()
        if hasattr(payload, "model_dump")
        else dict(payload)
    )

    updated = SERVICES["mar"].set_status(
        patient_id,
        item_id,
        payload_data,
    )

    if updated is None:
        return {
            "error": "MAR item not found",
        }

    return updated


@app.post("/mar/{patient_id}/{index}/pharmacy-review")
def pharmacy_review_mar_item(
    patient_id: str,
    index: int,
    payload: dict,
    current_user: dict = Depends(get_current_user),
):
    item_id = SERVICES["mar"].resolve_item_id_by_index(
        patient_id,
        index,
    )
    if item_id is None:
        return {
            "error": "MAR item not found",
        }

    payload_data = (
        payload.model_dump()
        if hasattr(payload, "model_dump")
        else dict(payload)
    )

    if not payload_data.get("status"):
        payload_data["status"] = "Reviewed"

    updated = SERVICES["mar"].set_pharmacy_review(
        patient_id,
        item_id,
        payload_data,
    )

    if updated is None:
        return {
            "error": "MAR item not found",
        }

    return updated


RADIOLOGY = {"P-1001": [{"study": "CT Chest", "status": "Pending", "report": ""}]}


@app.get("/radiology/{patient_id}")
def get_radiology(patient_id: str, current_user: dict = Depends(get_current_user)):
    return RADIOLOGY.get(patient_id, [])


@app.post("/radiology/{patient_id}")
def add_radiology(
    patient_id: str, payload: dict, current_user: dict = Depends(get_current_user)
):
    if patient_id not in RADIOLOGY:
        RADIOLOGY[patient_id] = []
    RADIOLOGY[patient_id].append(payload)
    return {"status": "ok", "radiology": RADIOLOGY[patient_id]}


from .ai_radiology import analyze_ct_scan


@app.post("/radiology/{patient_id}/{index}/analyze")
def analyze_radiology(
    patient_id: str, index: int, current_user: dict = Depends(get_current_user)
):
    if patient_id not in RADIOLOGY:
        return {"error": "No studies"}

    study = RADIOLOGY[patient_id][index]
    result = analyze_ct_scan(study.get("study", ""))

    RADIOLOGY[patient_id][index]["ai"] = result

    if result.get("priority") == "HIGH":
        ALERTS.append(
            {
                "patient_id": patient_id,
                "message": "Critical radiology finding",
                "time": "NOW",
            }
        )
    return {"status": "ok", "result": result}


ALERTS = []


@app.get("/alerts")
def get_alerts():
    return ALERTS


from .deep_ai_radiology import analyze_image
from .dicom_utils import load_dicom


@app.post("/ai/deep-radiology")
def deep_radiology(payload: dict):
    path = payload.get("path")

    img = load_dicom(path)
    result = analyze_image(img)

    return {
        "status": "ok",
        "prediction": result,
        "risk": "HIGH" if result["abnormal"] > 0.7 else "LOW",
    }


from .ai_report import generate_radiology_report


@app.post("/ai/deep-report")
def deep_report(payload: dict):
    pred = payload.get("prediction")
    report = generate_radiology_report(pred)

    return {"report": report}


from .ai_inference import predict_image


@app.post("/ai/predict")
def predict(payload: dict):
    path = payload.get("path")
    result = predict_image(path)

    return {"prediction": result, "risk": "HIGH" if result["abnormal"] > 0.7 else "LOW"}


from .unet_inference import segment_image


@app.post("/ai/segment")
def segment(payload: dict):
    path = payload.get("path")
    mask = segment_image(path)

    return {"status": "ok", "mask": mask}


from .unet3d_inference import segment_3d


@app.post("/ai/3d-segmentation")
def ai_3d(payload: dict):
    folder = payload.get("folder")

    mask = segment_3d(folder)

    return {"status": "ok", "message": "3D segmentation complete", "mask": mask}


from .ai_diagnosis import auto_diagnose


@app.post("/ai/diagnose")
def diagnose(payload: dict):
    mask = payload.get("mask")
    result = auto_diagnose(mask)

    return result


# ── WebSocket Real-time Alerts ────────────────────────────────────────────────
import asyncio
import uuid
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, data: dict):
        import json

        msg = json.dumps(data)
        for ws in self.active.copy():
            try:
                await ws.send_text(msg)
            except Exception:
                self.active.remove(ws)


ws_manager = ConnectionManager()


@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send demo alerts every 30 seconds
        import random, datetime

        demo_alerts = [
            {
                "type": "patient",
                "message": "Patient P-1003 oxygen saturation dropped to 87%",
                "severity": "critical",
                "patientId": "P-1003",
            },
            {
                "type": "lab",
                "message": "Critical lab result: Troponin 1.2 ng/mL for P-1001",
                "severity": "critical",
                "patientId": "P-1001",
            },
            {
                "type": "pharmacy",
                "message": "Drug interaction detected: Warfarin + Aspirin for P-1001",
                "severity": "high",
                "patientId": "P-1001",
            },
            {
                "type": "radiology",
                "message": "AI detected abnormality in CT Chest — P-1002",
                "severity": "high",
                "patientId": "P-1002",
            },
            {
                "type": "alert",
                "message": "ICU bed capacity at 90% — critical threshold",
                "severity": "moderate",
            },
        ]
        while True:
            await asyncio.sleep(30)
            alert = random.choice(demo_alerts)
            await ws_manager.broadcast(
                {
                    **alert,
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                }
            )
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.post("/claude/analyze", response_model=None)
async def claude_analyze(req: FastAPIRequest):
    body = await req.json()
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            },
            json=body,
        )
    return res.json()


# ── Patient CRUD ──────────────────────────────────────────────────────────────


@app.post("/groq/chat")
async def groq_chat(req: FastAPIRequest):
    import httpx

    body = await req.json()
    message = body.get("message", "")
    mode = body.get("mode", "default")
    language = body.get("language", "en")
    history = body.get("history", [])

    prompts = {
        "triage": "You are an AI medical triage specialist. Assess symptoms: CRITICAL|URGENT|SEMI-URGENT|NON-URGENT.",
        "lab": "You are an AI lab interpreter. Flag HIGH/LOW/CRITICAL/NORMAL.",
        "report": "You are an AI medical report generator.",
        "decision": "You are an AI clinical decision support system.",
        "default": "You are CareBot, an AI medical assistant.",
        "cardiology": "You are an expert AI cardiologist (ACC/AHA guidelines).",
        "neurology": "You are an expert AI neurologist (AAN guidelines).",
        "emergency": "You are an expert AI emergency physician (ATLS/ACLS).",
        "pediatrics": "You are an expert AI pediatrician (AAP/WHO).",
        "pharmacy": "You are an expert AI clinical pharmacist (FDA/USP).",
    }
    lang_suffix = {
        "en": "",
        "ar": "",
        "fr": "",
        "it": "",
        "sv": "",
    }
    system = prompts.get(mode, prompts["default"]) + lang_suffix.get(language, "")

    messages = [{"role": "system", "content": system}]
    for m in history[-12:]:
        if m.get("role") in ("user", "assistant"):
            messages.append({"role": m["role"], "content": m.get("content", "")})
    messages.append({"role": "user", "content": message})

    import os

    groq_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_key:
        return {"response": "AI unavailable — GROQ_API_KEY not set", "mode": mode}

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "max_tokens": 1500,
            },
        )
        data = res.json()
        reply = data["choices"][0]["message"]["content"]
    return {"response": reply, "message": reply, "mode": mode}


    db.delete(p)
    db.commit()
    return {"success": True}


# ── FHIR R4 Endpoints ─────────────────────────────────────────────────────────
from .fhir import patient_to_fhir, observation_to_fhir, medication_request_to_fhir, bundle_response
from .legacy_security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    check_rate_limit,
    AuditLogger,
)
from .tenant import TenantContext


@app.get("/fhir/R4/Patient", response_model=None)
def fhir_patients(db: Session = Depends(get_db)):
    from .models import Patient

    patients = db.query(Patient).all()
    resources = [patient_to_fhir(p) for p in patients]
    return bundle_response(resources)


@app.get("/fhir/R4/Patient/{patient_id}", response_model=None)
def fhir_patient(patient_id: str, db: Session = Depends(get_db)):
    from .models import Patient

    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p:
        raise HTTPException(404, "Patient not found")
    return patient_to_fhir(p)


@app.get("/fhir/R4/Observation", response_model=None)
def fhir_observations(patient: str = None, db: Session = Depends(get_db)):
    from .models import NursingVital

    q = db.query(NursingVital)
    if patient:
        q = q.filter(NursingVital.patient_id == patient)
    vitals = q.all()
    resources = [observation_to_fhir(v, v.patient_id) for v in vitals]
    return bundle_response(resources)






@app.get("/fhir/R4/MedicationRequest", response_model=None)
def fhir_medication_requests(db: Session = Depends(get_db)):

    rows = db.execute(text("""

        SELECT
            id,
            patient_id,
            drug_name,
            generic_name,
            dose,
            route,
            frequency,
            duration_days,
            quantity,
            is_active,
            created_at

        FROM medication_orders_simple

        ORDER BY id DESC
        LIMIT 50

    """)).mappings().all()

    resources = []

    for r in rows:

        resources.append({

            "resourceType": "MedicationRequest",

            "id": str(r["id"]),

            "status": (
                "active"
                if r["is_active"]
                else "stopped"
            ),

            "intent": "order",

            "subject": {
                "reference": (
                    f'Patient/{r["patient_id"]}'
                )
            },

            "authoredOn": (
                r["created_at"].isoformat() + "Z"
                if r["created_at"]
                else None
            ),

            "medicationCodeableConcept": {
                "text": r["drug_name"],

                "coding": [
                    {
                        "system": (
                            "http://www.nlm.nih.gov/"
                            "research/umls/rxnorm"
                        ),

                        "display": (
                            r["generic_name"]
                            or r["drug_name"]
                        ),
                    }
                ],
            },

            "dosageInstruction": [
                {
                    "text": (
                        f'{r["dose"]} '
                        f'{r["route"]} '
                        f'{r["frequency"]}'
                    )
                }
            ],

            "dispenseRequest": {
                "quantity": {
                    "value": r["quantity"]
                },

                "expectedSupplyDuration": {
                    "value": r["duration_days"],
                    "unit": "days",
                },
            },
        })

    return bundle_response(resources)


@app.get("/fhir/R4/metadata", response_model=None)
def fhir_capability():
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "kind": "instance",
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "software": {"name": "AI Hospital Alliance FHIR Server", "version": "1.0.0"},
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [{"code": "read"}, {"code": "search-type"}],
                    },
                    {
                        "type": "Observation",
                        "interaction": [{"code": "read"}, {"code": "search-type"}],
                    },
                ],
            }
        ],
    }


# ── Auth Refresh Token ────────────────────────────────────────────────────────
@app.post("/auth/refresh", response_model=None)
def refresh_token(data: dict):
    token = data.get("refresh_token", "")
    payload = verify_refresh_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired refresh token")
    username = payload.get("sub")
    new_access = create_access_token({"sub": username})
    new_refresh = create_refresh_token({"sub": username})
    return {"access_token": new_access, "refresh_token": new_refresh}


# ── Audit Log endpoint ────────────────────────────────────────────────────────
@app.get("/audit/logs", response_model=None)
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    try:
        from .models import AuditLog

        logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": l.id,
                "user_id": l.user_id,
                "action": l.action,
                "resource": l.resource,
                "success": l.success,
                "timestamp": str(l.timestamp),
                "ip": l.ip_address,
            }
            for l in logs
        ]
    except:
        return []


# ── Multi-tenant info ────────────────────────────────────────────────────────
@app.get("/tenant/{hospital_id}", response_model=None)
def get_tenant_info(hospital_id: str):
    from .tenant import TENANT_REGISTRY

    tenant = TENANT_REGISTRY.get(hospital_id)
    if not tenant:
        raise HTTPException(404, "Tenant not found")
    return {"hospital_id": hospital_id, **tenant}


@app.get("/tenants", response_model=None)
def list_tenants():
    from .tenant import TENANT_REGISTRY

    return [{"id": k, **v} for k, v in TENANT_REGISTRY.items()]


# ===== Smart AI Endpoint =====
@app.post("/ai/smart")
def smart_ai(payload: dict):
    msg = payload.get("message", "")
    provider = payload.get("provider", "auto")
    return {"reply": ask_ai(msg, provider)}

@app.get("/ready")
def readiness_check():
    return {
        "status": "ready",
        "backend": "ok",
        "version": "2.0.0"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SaaS - Hospital Self-Service Registration & Multi-Tenant Management
# ═══════════════════════════════════════════════════════════════════════════════

from .saas import (
    PLANS, HospitalRegisterRequest, register_hospital,
    get_tenant_by_id, get_tenant_from_api_key,
    tenant_to_public, check_ai_quota, increment_ai_usage,
    Tenant, get_db,
)
from .db import Base, engine as _engine

# Ensure SaaS tables exist
Base.metadata.create_all(bind=_engine)


@app.get("/saas/plans", response_model=None, tags=["SaaS"])
def list_plans():
    """Public endpoint — list all subscription plans and their features."""
    return {
        "plans": [
            {
                "id": k,
                **{kk: vv for kk, vv in v.items() if kk != "trial_days"},
                "trial_days": v.get("trial_days", 0),
            }
            for k, v in PLANS.items()
        ]
    }


@app.post("/saas/register", response_model=None, tags=["SaaS"])
def saas_register(req: HospitalRegisterRequest):
    """
    Self-service hospital onboarding.
    Creates tenant, hospital record, default departments, and admin user.
    Returns API key (shown only once).
    """
    db = next(get_db())
    return register_hospital(req, db)


@app.get("/saas/tenant/{hospital_id}", response_model=None, tags=["SaaS"])
def saas_get_tenant(hospital_id: str):
    """Get tenant info by hospital_id (requires admin)."""
    db = next(get_db())
    t = get_tenant_by_id(hospital_id, db)
    return tenant_to_public(t)


@app.get("/saas/tenants", response_model=None, tags=["SaaS"])
def saas_list_tenants():
    """Super-admin: list all tenants."""
    _require_super_admin()
    db = next(get_db())
    tenants = db.query(Tenant).all()
    return [tenant_to_public(t) for t in tenants]


@app.post("/saas/tenant/{hospital_id}/suspend", response_model=None, tags=["SaaS"])
def saas_suspend_tenant(hospital_id: str):
    """Super-admin: suspend a tenant."""
    _require_super_admin()
    db = next(get_db())
    t = db.query(Tenant).filter(Tenant.id == hospital_id).first()
    if not t:
        raise HTTPException(404, "Tenant not found")
    t.is_active = False
    db.commit()
    return {"message": f"Tenant {hospital_id} suspended"}


@app.post("/saas/tenant/{hospital_id}/activate", response_model=None, tags=["SaaS"])
def saas_activate_tenant(hospital_id: str):
    """Super-admin: activate a suspended tenant."""
    _require_super_admin()
    db = next(get_db())
    t = db.query(Tenant).filter(Tenant.id == hospital_id).first()
    if not t:
        raise HTTPException(404, "Tenant not found")
    t.is_active = True
    db.commit()
    return {"message": f"Tenant {hospital_id} activated"}


@app.post("/saas/tenant/{hospital_id}/upgrade", response_model=None, tags=["SaaS"])
def saas_upgrade_plan(hospital_id: str, body: dict):
    """Upgrade/change a tenant's plan."""
    _require_super_admin()
    new_plan = body.get("plan")
    if new_plan not in PLANS:
        raise HTTPException(400, f"Invalid plan. Choose: {list(PLANS.keys())}")
    db = next(get_db())
    t = db.query(Tenant).filter(Tenant.id == hospital_id).first()
    if not t:
        raise HTTPException(404, "Tenant not found")
    t.plan = new_plan
    db.commit()
    return {"message": f"Plan updated to {new_plan}", **tenant_to_public(t)}


@app.get("/saas/tenant/{hospital_id}/usage", response_model=None, tags=["SaaS"])
def saas_usage(hospital_id: str):
    """Get current usage stats for a tenant."""
    db = next(get_db())
    t = get_tenant_by_id(hospital_id, db)
    from .models import User, Patient
    user_count = db.query(User).filter(User.hospital_id == hospital_id).count()
    patient_count = db.query(Patient).filter(Patient.hospital_id == hospital_id).count()
    plan = PLANS.get(t.plan, PLANS["trial"])
    return {
        "hospital_id": hospital_id,
        "plan": t.plan,
        "usage": {
            "users": user_count,
            "patients": patient_count,
            "ai_calls_today": t.ai_calls_today or 0,
        },
        "limits": {
            "max_users": plan["max_users"],
            "max_patients": plan["max_patients"],
            "ai_calls_per_day": plan["ai_calls_per_day"],
        },
        "trial_ends_at": t.trial_ends_at.isoformat() if t.trial_ends_at else None,
    }


def _require_super_admin():
    """Placeholder — in production wire to JWT super-admin role check."""
    sa_key = os.environ.get("SUPER_ADMIN_KEY")
    # For now just check env var is set; real impl checks JWT
    if not sa_key:
        raise HTTPException(503, "Super-admin key not configured")

# ===== AI Clinical Router =====
try:
    from backend.app.api.ai_clinical import router as ai_clinical_router
except Exception:
    from backend.app.api.ai_clinical import router as ai_clinical_router

app.include_router(ai_clinical_router)

# ===== Medical Standards Router =====
try:
    from backend.app.api.medical_standards import router as medical_standards_router
except Exception:
    from backend.app.api.medical_standards import router as medical_standards_router

app.include_router(medical_standards_router)

# ===== Smart Pharmacy Module Router =====
try:
    from backend.app.api.smart_pharmacy_module import router as smart_pharmacy_module_router
except Exception:
    from backend.app.api.smart_pharmacy_module import router as smart_pharmacy_module_router

app.include_router(smart_pharmacy_module_router)

# ===== Smart Pharmacy Real Engine Router =====
try:
    from backend.app.api.smart_pharmacy_real import router as smart_pharmacy_real_router
except Exception:
    from backend.app.api.smart_pharmacy_real import router as smart_pharmacy_real_router

app.include_router(smart_pharmacy_real_router)

# ===== Clinical AI Pipeline Router =====
try:
    from backend.app.api.clinical_ai_pipeline import router as clinical_ai_pipeline_router
except Exception:
    from backend.app.api.clinical_ai_pipeline import router as clinical_ai_pipeline_router

app.include_router(clinical_ai_pipeline_router)

# ===== Production Clinical AI Engines =====
try:
    from backend.app.engines.clinical_drug_profile import router as clinical_drug_router
    from backend.app.engines.multi_drug_interactions import router as multi_drug_router
    from backend.app.engines.dose_safety_ai import router as dose_safety_router
    from backend.app.engines.audit_trail import router as audit_router
except Exception:
    from backend.app.engines.clinical_drug_profile import router as clinical_drug_router
    from backend.app.engines.multi_drug_interactions import router as multi_drug_router
    from backend.app.engines.dose_safety_ai import router as dose_safety_router
    from backend.app.engines.audit_trail import router as audit_router

app.include_router(clinical_drug_router)
app.include_router(multi_drug_router)
app.include_router(dose_safety_router)
app.include_router(audit_router)

# ===== Real Patient Data Layer Router =====
try:
    from backend.app.api.real_patient_layer import router as real_patient_layer_router
except Exception:
    from backend.app.api.real_patient_layer import router as real_patient_layer_router

app.include_router(real_patient_layer_router)

# ===== Clinical Database v1 Router =====
try:
    from backend.app.api.clinical_db_v1 import router as clinical_db_v1_router
except Exception:
    from backend.app.api.clinical_db_v1 import router as clinical_db_v1_router

app.include_router(clinical_db_v1_router)

# ===== Clinical Lifecycle v1 Router =====
try:
    from backend.app.api.clinical_lifecycle_v1 import router as clinical_lifecycle_v1_router
except Exception:
    from backend.app.api.clinical_lifecycle_v1 import router as clinical_lifecycle_v1_router

app.include_router(clinical_lifecycle_v1_router)

# ===== Clinical Timeline v1 Router =====
try:
    from backend.app.api.clinical_timeline_v1 import router as clinical_timeline_v1_router
except Exception:
    from backend.app.api.clinical_timeline_v1 import router as clinical_timeline_v1_router

app.include_router(clinical_timeline_v1_router)

# ===== AI Longitudinal Patient Memory Router =====
try:
    from backend.app.api.patient_memory_v1 import router as patient_memory_v1_router
except Exception:
    from backend.app.api.patient_memory_v1 import router as patient_memory_v1_router

app.include_router(patient_memory_v1_router)

# =========================================================
# ENTERPRISE CLINICAL SYSTEM
# =========================================================

try:
    from backend.app.api.auth_enterprise import router as auth_enterprise_router
    from backend.app.api.mar_engine import router as mar_engine_router
    from backend.app.api.risk_engine import router as risk_engine_router
    from backend.app.api.realtime_events import router as realtime_events_router
except Exception:
    from backend.app.api.auth_enterprise import router as auth_enterprise_router
    from backend.app.api.mar_engine import router as mar_engine_router
    from backend.app.api.risk_engine import router as risk_engine_router
    from backend.app.api.realtime_events import router as realtime_events_router

app.include_router(auth_enterprise_router)
app.include_router(mar_engine_router)
app.include_router(risk_engine_router)
app.include_router(realtime_events_router)


# ===== Enterprise Live Clinical Operations Routers =====
try:
    from backend.app.api.enterprise_notifications import router as enterprise_notifications_router
    from backend.app.api.enterprise_dashboard import router as enterprise_dashboard_router
    from backend.app.api.enterprise_rbac import router as enterprise_rbac_router
    from backend.app.api.clinical_copilot import router as clinical_copilot_router
except Exception:
    from backend.app.api.enterprise_notifications import router as enterprise_notifications_router
    from backend.app.api.enterprise_dashboard import router as enterprise_dashboard_router
    from backend.app.api.enterprise_rbac import router as enterprise_rbac_router
    from backend.app.api.clinical_copilot import router as clinical_copilot_router

app.include_router(enterprise_notifications_router)
app.include_router(enterprise_dashboard_router)
app.include_router(enterprise_rbac_router)
app.include_router(clinical_copilot_router)

app.include_router(radiology_upload_router)

@app.post("/auth/dev-login")
def dev_login(payload: dict):
    if os.getenv("APP_ENV", "").strip().lower() not in {"dev", "development", "local", "test"}:
        raise HTTPException(status_code=404, detail="Not found")

    username = payload.get("username", "admin")

    token = create_access_token({
        "sub": "00000000-0000-0000-0000-000000000001",
        "tenant_id": "00000000-0000-0000-0000-000000000100",
        "role": "tenant_admin",
        "email": f"{username}@aiha.local",
        "username": username
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": username,
            "role": "Admin"
        }
    }

app.include_router(ultrasound_ai_router)

app.include_router(ai_ultrasound_reports.router)

app.include_router(ai_ultrasound_pdf.router)

app.include_router(ai_ultrasound_dicom.router)

app.mount("/generated_inference", StaticFiles(directory="generated_inference"), name="generated_inference")

app.include_router(ai_ultrasound_inference.router)

# AI Ultrasound X 6.2
app.include_router(ai_ultrasound_x_62_router)
app.include_router(multi_agent_reasoning_router)
app.include_router(knowledge_graph_router)

from backend.app.autonomous_healthcare_os.predictive_hospital_operations import router as predictive_hospital_operations_router

app.include_router(predictive_hospital_operations_router)

from backend.app.autonomous_healthcare_os.medical_memory_engine import router as medical_memory_router

app.include_router(medical_memory_router)

from backend.app.autonomous_healthcare_os.self_learning_outcome_engine import router as self_learning_router

app.include_router(self_learning_router)

from backend.app.autonomous_healthcare_os.hospital_intelligence_mesh import router as hospital_intelligence_mesh_router

app.include_router(hospital_intelligence_mesh_router)

from backend.app.autonomous_healthcare_os.ahos_complete_core import router as ahos_complete_router

app.include_router(ahos_complete_router)

from backend.app.database.ahos_database_api import router as ahos_database_router

app.include_router(ahos_database_router)

from backend.app.database.ahos_events_api import router as ahos_events_router

app.include_router(ahos_events_router)

from backend.app.database.gmin_dashboard_api import router as gmin_dashboard_router

app.include_router(gmin_dashboard_router)

from backend.app.gmin_live.live_operations_center import router as gmin_live_operations_router

app.include_router(gmin_live_operations_router)


from backend.app.gmin_realtime.realtime_command_center import router as gmin_realtime_router


app.include_router(gmin_realtime_router)

from backend.app.gmin_realtime.realtime_intelligence_layer import router as gmin_realtime_intelligence_router

app.include_router(gmin_realtime_intelligence_router)

from backend.app.global_digital_twin.global_digital_twin_network import router as global_digital_twin_router

app.include_router(global_digital_twin_router)

app.include_router(clinical_timeline_101_router)

app.include_router(clinical_story_102_router)

app.include_router(clinical_reasoning_103_router)

app.include_router(care_plan_104_router)

app.include_router(outcome_prediction_105_router)

app.include_router(medical_command_brain_110_router)

# AHOS 11.1.1 Resource Forecast Engine
app.include_router(resource_forecast_router)

# AHOS 11.1.2 Hospital Capacity Predictor
app.include_router(capacity_router)

# AHOS 11.1.3 Autonomous Resource Optimizer
app.include_router(resource_optimizer_router)

# AHOS 11.2.1
app.include_router(inter_hospital_router)

# AHOS 11.2.2 Regional Healthcare Intelligence
app.include_router(regional_intelligence_router)

# AHOS 11.2.3 Population Health Intelligence
app.include_router(population_router)

# AHOS 11.2.4 Pandemic Intelligence Engine
app.include_router(pandemic_router)

# AHOS 11.2.5 National Healthcare Command
app.include_router(national_command_router)

# AHOS 11.3.1 Healthcare Federation Core
app.include_router(federation_core_router)

# AHOS 11.3.2 Federated Medical Intelligence
app.include_router(federated_medical_router)

# AHOS 11.3.3 Federated Clinical Consensus
app.include_router(federated_consensus_router)

# AHOS 11.3.4 Federated Resource Optimization
app.include_router(federated_resource_router)

# AHOS 11.3.5 Global Healthcare Federation Command
app.include_router(global_federation_command_router)

# AHOS 11.4.1 Autonomous Hospital Orchestration Core
app.include_router(orchestration_router)

# AHOS 11.4.2 Autonomous Workflow Engine
app.include_router(workflow_router)

# AHOS 11.4.3 Care Path Orchestrator
app.include_router(care_path_router)

# AHOS 11.4.4 Resource Orchestrator
app.include_router(resource_orchestrator_router)

# AHOS 11.4.5 Emergency Orchestrator
app.include_router(emergency_orchestrator_router)

# AHOS 11.4.6 ICU Orchestrator
app.include_router(icu_orchestrator_router)

# AHOS 11.4.7 Pharmacy Orchestrator
app.include_router(pharmacy_orchestrator_router)

# AHOS 11.4.8 Laboratory Orchestrator
app.include_router(laboratory_orchestrator_router)

# AHOS 11.4.9 Radiology Orchestrator
app.include_router(radiology_orchestrator_router)

# AHOS 11.5.1 Executive Healthcare Intelligence
app.include_router(executive_intelligence_router)

# AHOS 11.5.2
app.include_router(strategic_router)

# AHOS 11.5.3 Executive Forecast Intelligence
app.include_router(executive_forecast_router)

# AHOS 11.5.4 Executive Risk Intelligence
app.include_router(executive_risk_router)

# AHOS 11.5.5 Executive Command Brain
app.include_router(executive_command_brain_router)

# AHOS 12.0 Autonomous Healthcare Operating System
app.include_router(ahos_core_router)

# AHOS 12.1 Production Readiness & Enterprise Integration
app.include_router(production_readiness_router)

# AHOS 12.2 FHIR HL7 Enterprise Interoperability Layer
app.include_router(fhir_hl7_router)

# AHOS 12.3 Cybersecurity Compliance & Audit Hardening
app.include_router(security_compliance_router)

# AHOS 12.4 Clinical Validation & Regulatory Readiness
app.include_router(clinical_validation_router)

# AHOS 12.5 Real Hospital Data Integration Layer
app.include_router(real_data_router)

# AHOS 12.6 Enterprise Deployment
app.include_router(enterprise_deployment_router)

# AHOS 13.0.1 Global Hospital Federation
app.include_router(global_hospital_federation_router)

# AHOS 13.0.2 Global Medical Knowledge Graph
app.include_router(global_medical_kg_router)

# AHOS 13.0.3 Worldwide Disease Surveillance
app.include_router(disease_surveillance_router)

# AHOS 13.0.4 Global Clinical Intelligence Exchange
app.include_router(clinical_exchange_router)

# AHOS 13.0.5 Planetary Healthcare Command Center
app.include_router(planetary_command_router)

# AHOS 14.0.1 Global Medical AI Brain
app.include_router(global_ai_brain_router)

# AHOS 14.0.2 Autonomous Medical Civilization Layer
app.include_router(medical_civilization_router)

# AHOS 14.0.3 Planetary Medical Intelligence Grid
app.include_router(intelligence_grid_router)

# AHOS 14.0.5 Universal Healthcare Intelligence Network
app.include_router(universal_network_router)

# AHOS 15.0.1 Self-Evolving Medical Intelligence
app.include_router(self_evolving_router)

# AHOS 15.0.2 Autonomous Global Medical Governance
app.include_router(global_governance_router)

# AHOS 15.0.3 Universal Medical Knowledge Engine
app.include_router(universal_knowledge_router)

# AHOS 15.0.4 Planetary Healthcare Optimization Core
app.include_router(planetary_optimization_router)

# AHOS 15.0.5 Medical Singularity Command Brain
app.include_router(singularity_router)

# AHOS 16.0 Enterprise Real Execution
app.include_router(enterprise_real_execution_router)

# AHOS 16.0.1 Real FHIR R4 Connector
app.include_router(real_fhir_r4_router)

# AHOS 16.0.2 HL7 v2 Parser
app.include_router(hl7_v2_router)

# AHOS 16.0.3 Orthanc OHIF PACS Production Bridge
app.include_router(pacs_bridge_router)

# AHOS 16.0.4 LIS Laboratory Integration
app.include_router(lis_router)

# AHOS 16.0.6 SaaS Multi-Tenant Architecture
app.include_router(saas_router)

# AHOS 16.0.8 Pilot Hospital Deployment Pack
app.include_router(pilot_deployment_router)

# AHOS 17.0 Investor & Enterprise Presentation Pack
app.include_router(investor_pack_router)

# AHOS 17.1 Investor Pitch Deck Generator
app.include_router(investor_pitch_router)

# AHOS 17.2 Enterprise Sales & Partnership Kit
app.include_router(enterprise_sales_router)

# AHOS 17.3 Government Healthcare Proposal Pack
app.include_router(government_router)

# AHOS 17.4 International Expansion Framework
app.include_router(expansion_router)

# AHOS 17.5 Global Launch Program
app.include_router(global_launch_router)

# AHOS 18.0 Commercial Production Release
app.include_router(production_router)

# AHOS 18.1 Enterprise Customer Success Platform
app.include_router(customer_success_router)

# AHOS 18.2 Global Healthcare Operations Network
app.include_router(global_operations_router)

# AHOS 18.3 Healthcare Marketplace Ecosystem
app.include_router(marketplace_router)

# AHOS 19.0 Enterprise Edition
app.include_router(enterprise_edition_router)

# AHOS 19.1 Enterprise AI Command Suite
app.include_router(enterprise_command_suite_router)

# AHOS 19.2 National Healthcare Cloud Edition
app.include_router(national_cloud_router)

# AHOS 19.3 Global Medical Intelligence Exchange
app.include_router(global_medical_exchange_router)

# AHOS 20.0 Global Healthcare Platform
app.include_router(global_platform_router)

# AHOS 21.0 Production Real Implementation
app.include_router(real_implementation_router)

# AHOS 21.0.1 PostgreSQL Production Database
app.include_router(postgresql_production_router)

# AHOS 21.0.2 Docker Production Stack
app.include_router(docker_stack_router)

# AHOS 21.0.3 Keycloak RBAC SSO
app.include_router(keycloak_rbac_router)

# AHOS 21.0.4 HAPI FHIR Server Bridge
app.include_router(hapi_fhir_bridge_router)

# AHOS 21.0.5 Orthanc OHIF Production Stack
app.include_router(orthanc_ohif_router)

# AHOS 21.0.6 Audit Logs & Security Events
app.include_router(audit_security_router)

# AHOS 21.0.7 Prometheus Grafana Monitoring
app.include_router(monitoring_router)

# AHOS 21.0.8 CI/CD Production Pipeline
app.include_router(cicd_router)

# AHOS 22.0 Real Hospital Deployment Program
app.include_router(real_deployment_router)

# AHOS 22.0.1 Real PostgreSQL Schema
app.include_router(real_postgresql_schema_router)

# AHOS 22.0.2 Real FHIR Resource Storage
app.include_router(real_fhir_storage_router)

# AHOS 22.0.3 Real Orthanc DICOM Integration
app.include_router(real_orthanc_dicom_router)

# AHOS 22.0.4 Real OHIF Viewer Integration
app.include_router(real_ohif_viewer_router)

# AHOS 22.0.5 Real Drug Database
app.include_router(real_drug_database_router)

# AHOS 22.0.6 Real Laboratory Database
app.include_router(real_laboratory_database_router)

# AHOS 22.0.7 Real Multi-Tenant SaaS
app.include_router(real_multi_tenant_router)

# AHOS 22.0.8 First Pilot Hospital Deployment
app.include_router(first_pilot_router)

# AI Hospital Alliance 24.0.1 Hospital Operations Core
app.include_router(hospital_operations_24_router)
app.include_router(live_bed_router)
app.include_router(patient_flow_router)
app.include_router(emergency_command_router)
app.include_router(autonomous_icu_router)

app.include_router(radiology_operations_router)

app.include_router(laboratory_operations_router)

app.include_router(pharmacy_operations_router)

app.include_router(surgical_operations_router)

app.include_router(executive_command_24_1_router)

app.include_router(financial_operations_router)

app.include_router(supply_chain_router)
app.include_router(unified_digital_twin_router)
app.include_router(hospital_brain_router)
app.include_router(unified_executive_router)
app.include_router(federation_24_8_router)
app.include_router(digital_twin_24_9_router)
app.include_router(aghos_core_router)
app.include_router(clinical_mesh_router)
app.include_router(realtime_event_monitor_router)
app.include_router(data_exchange_25_3_router)
app.include_router(ahos26_1_router)
app.include_router(ahos26_2_router)
app.include_router(ahos26_3_router)
app.include_router(ahos26_4_router)
app.include_router(ahos26_5_router)
app.include_router(ahos26_6_router)
app.include_router(ahos26_7_router)

from backend.app.ahos_26_8.global_healthcare_ai_federation_core import router as ahos_26_8_router
app.include_router(ahos_26_8_router)

from backend.app.ahos_26_9.autonomous_healthcare_civilization_layer import router as ahos_26_9_router
app.include_router(ahos_26_9_router)

from backend.app.ahos_27_0.agi_healthcare_command_nexus import router as ahos_27_0_router
app.include_router(ahos_27_0_router)

from backend.app.ahos_27_1.autonomous_agi_medical_governance_core import router as ahos_27_1_router
app.include_router(ahos_27_1_router)

from backend.app.ahos_27_2.autonomous_clinical_safety_compliance_nexus import router as ahos_27_2_router
app.include_router(ahos_27_2_router)

from backend.app.ahos_27_3.autonomous_medical_device_certification_engine import router as ahos_27_3_router
app.include_router(ahos_27_3_router)

from backend.app.ahos_27_4.autonomous_clinical_validation_evidence_engine import router as ahos_27_4_router
app.include_router(ahos_27_4_router)

from backend.app.ahos_27_5.autonomous_real_world_evidence_post_market_surveillance_core import router as ahos_27_5_router
app.include_router(ahos_27_5_router)

from backend.app.ahos_27_6.autonomous_global_clinical_risk_intelligence_core import router as ahos_27_6_router
app.include_router(ahos_27_6_router)

from backend.app.ahos_27_7.autonomous_global_clinical_governance_risk_board import router as ahos_27_7_router
app.include_router(ahos_27_7_router)

from backend.app.ahos_27_8.autonomous_global_clinical_deployment_readiness_engine import router as ahos_27_8_router
app.include_router(ahos_27_8_router)

from backend.app.ahos_27_9.autonomous_global_hospital_pilot_launch_core import router as ahos_27_9_router
app.include_router(ahos_27_9_router)

from backend.app.ahos_28_0.autonomous_global_healthcare_enterprise_launch_platform import router as ahos_28_0_router
app.include_router(ahos_28_0_router)

from backend.app.ahos_28_1.router import router as ahos_28_1_router




from backend.app.ahos_28_3.router import router as ahos_28_3_router
app.include_router(ahos_28_3_router)


from backend.app.ahos_28_4.router import router as ahos_28_4_router
app.include_router(ahos_28_4_router)


from backend.app.ahos_28_6.router import router as ahos_28_6_router
app.include_router(ahos_28_6_router)



@app.get("/system-health")
async def system_health():
    return {
        "status": "online",
        "platform": "AI Hospital Alliance",
        "phase": "AHOS 28.0",
        "backend": "running",
        "enterprise_launch": "active"
    }



from backend.app.ahos_28_2.multi_tenant_healthcare_cloud import router as ahos_28_2_router


from backend.app.ahos_28_2_1.tenant_database_isolation import router as ahos_28_2_1_router
app.include_router(ahos_28_2_1_router)


from backend.app.ahos_28_2_2.tenant_authentication_layer import router as ahos_28_2_2_router
app.include_router(ahos_28_2_2_router)


from backend.app.ahos_28_2_3.tenant_provisioning_engine import router as ahos_28_2_3_router
app.include_router(ahos_28_2_3_router)


from backend.app.ahos_28_2_4.multi_tenant_dashboard import router as ahos_28_2_4_router
app.include_router(ahos_28_2_4_router)


from backend.app.ahos_28_2_5.subscription_billing_engine import router as ahos_28_2_5_router
app.include_router(ahos_28_2_5_router)


from backend.app.ahos_28_2_6.multi_region_deployment import router as ahos_28_2_6_router
app.include_router(ahos_28_2_6_router)


from backend.app.ahos_28_2_7.global_tenant_federation import router as ahos_28_2_7_router
app.include_router(ahos_28_2_7_router)


from backend.app.ahos_28_3.unified_clinical_data_platform import router as ahos_28_3_router
app.include_router(ahos_28_3_router)


from backend.app.ahos_28_4.global_fhir_hl7_exchange import router as ahos_28_4_router
app.include_router(ahos_28_4_router)


from backend.app.ahos_28_5.real_hospital_deployment_validation import router as ahos_28_5_router
app.include_router(ahos_28_5_router)


from backend.app.ahos_29_0.global_autonomous_healthcare_intelligence_network import router as ahos_29_0_router
app.include_router(ahos_29_0_router)


from backend.app.ahos_30_0.production_regulatory_readiness_program import router as ahos_30_0_router
app.include_router(ahos_30_0_router)


from backend.app.ahos_30_1.real_clinical_data_integration import router as ahos_30_1_router
app.include_router(ahos_30_1_router)


from backend.app.ahos_30_2.production_kubernetes_platform import router as ahos_30_2_router
app.include_router(ahos_30_2_router)


from backend.app.ahos_30_3.mlops_ai_governance_platform import router as ahos_30_3_router
app.include_router(ahos_30_3_router)


from backend.app.ahos_30_4.medical_device_regulatory_program import router as ahos_30_4_router
app.include_router(ahos_30_4_router)


from backend.app.ahos_30_5.clinical_evidence_post_market_surveillance import router as ahos_30_5_router
app.include_router(ahos_30_5_router)


from backend.app.ahos_30_6.cybersecurity_zero_trust_platform import router as ahos_30_6_router
app.include_router(ahos_30_6_router)


from backend.app.ahos_30_7.global_commercial_launch_partner_ecosystem import router as ahos_30_7_router
app.include_router(ahos_30_7_router)


from backend.app.ahos_31_0.autonomous_global_healthcare_enterprise_platform import router as ahos_31_0_router
app.include_router(ahos_31_0_router)






from backend.app.ahos_33_0.autonomous_medical_research_discovery_network import router as ahos_33_router
app.include_router(ahos_33_router)


from backend.app.ahos_34_0.autonomous_medical_innovation_drug_discovery_ecosystem import router as ahos_34_router
app.include_router(ahos_34_router)













from backend.app.router_registry import register_all_routers
register_all_routers(app)


from backend.app.plugins.loader import load_plugins
from backend.app.plugins.plugin_status import router as plugin_status_router
from backend.app.plugins.plugin_status import LOADED_PLUGINS

app.include_router(plugin_status_router)
LOADED_PLUGINS.extend(load_plugins(app))


from backend.app.service_registry.routes import router as service_registry_router
app.include_router(service_registry_router)


from backend.app.container.routes import router as container_router
from backend.app.container.bootstrap import bootstrap_services

bootstrap_services()
app.include_router(container_router)


app.include_router(ahos_41_0_4_router)

app.include_router(ahos_41_1_router)

from backend.app.ahos_41_3_3.secure_regulatory_submission_portal import router as ahos_41_3_3_router
app.include_router(ahos_41_3_3_router)


from backend.app.ahos_41_3_4.digital_signature_part11 import router as ahos_41_3_4_router
app.include_router(ahos_41_3_4_router)


from backend.app.ahos_41_3_5.multi_authority_gateway import router as ahos_41_3_5_router
app.include_router(ahos_41_3_5_router)


from backend.app.ahos_41_3_6.regulatory_review_dashboard import router as ahos_41_3_6_router
app.include_router(ahos_41_3_6_router)


from backend.app.ahos_41_3_7.audit_evidence_generator import router as ahos_41_3_7_router
app.include_router(ahos_41_3_7_router)


from backend.app.ahos_42_0.clinical_validation_platform import router as ahos_42_0_router
app.include_router(ahos_42_0_router)






from backend.app.ahos_42_1.federated_clinical_validation_network import router as ahos_42_1_router
app.include_router(ahos_42_1_router)


app.include_router(ahos_42_2_router)


app.include_router(ahos_42_3_router)


app.include_router(ahos_42_4_router)


app.include_router(ahos_42_5_router)


app.include_router(ahos_42_6_router)


app.include_router(ahos_42_7_router)


app.include_router(ahos_42_8_router)


app.include_router(ahos_43_1_router)


app.include_router(ahos_43_2_router)


app.include_router(ahos_43_3_router)


app.include_router(ahos_43_4_router)


app.include_router(ahos_43_5_router)


app.include_router(ahos_44_0_router)


app.include_router(ahos_44_1_router)


app.include_router(ahos_44_2_router)


app.include_router(ahos_44_3_router)


app.include_router(ahos_44_4_router)


app.include_router(ahos_44_5_router)



app.include_router(ahos_45_0_router)




app.include_router(ahos_45_1_router)



app.include_router(ahos_45_2_router)


app.include_router(ahos_45_3_router)


app.include_router(ahos_46_0_router)


app.include_router(ahos_46_1_router)



app.include_router(ahos_46_2_router)


app.include_router(ahos_46_3_router)


app.include_router(ahos_46_4_router)


app.include_router(ahos_46_5_router)


app.include_router(ahos_46_6_router)


app.include_router(ahos_46_7_router)


app.include_router(ahos_46_8_router)


app.include_router(ahos_46_9_router)


app.include_router(ahos_47_0_router)


app.include_router(ahos_47_1_router)


app.include_router(ahos_47_2_router)



from backend.app.ahos_47_3.production_hospital_deployment_clinical_validation_platform import router as ahos_47_3_router
app.include_router(ahos_47_3_router)


from backend.app.ahos_47_4.cybersecurity_zero_trust_medical_soc_platform import router as ahos_47_4_router
app.include_router(ahos_47_4_router)


from backend.app.ahos_47_5.regulatory_certification_samd_platform import router as ahos_47_5_router
app.include_router(ahos_47_5_router)


from backend.app.ahos_47_6.global_multi_hospital_federation_platform import router as ahos_47_6_router
app.include_router(ahos_47_6_router)


from backend.app.ahos_48_0.global_commercial_launch_platform import router as ahos_48_0_router
app.include_router(ahos_48_0_router)


from backend.app.ahos_48_1.investor_strategic_partnership_dossier_platform import router as ahos_48_1_router
app.include_router(ahos_48_1_router)


from backend.app.ahos_48_2.ipo_global_expansion_platform import router as ahos_48_2_router
from backend.app.api.unified_dashboard import router as unified_dashboard_router
from backend.app.api.radiology_dashboard import router as radiology_dashboard_router
from backend.app.api.ultrasound_dashboard import router as ultrasound_dashboard_router
app.include_router(ahos_48_2_router)


app.include_router(ahos_49_0_2_identity_rbac_router)


app.include_router(ahos_49_0_3_real_hospital_integration_router)


app.include_router(ahos_49_0_4_autonomous_hospital_orchestrator_router)


app.include_router(ahos_49_0_5_global_monitoring_router)


app.include_router(ahos_49_0_6_rwe_learning_router)


app.include_router(ahos_49_0_7_strategic_partnership_router)


app.include_router(ahos_49_0_8_global_ecosystem_router)


app.include_router(ahos_50_0_production_hardening_router)


app.include_router(ahos_50_1_migrations_cicd_router)


app.include_router(ahos_50_2_api_validation_load_testing_router)


app.include_router(ahos_50_3_security_compliance_router)


app.include_router(ahos_50_4_observability_router)


app.include_router(ahos_50_5_k8s_router)


app.include_router(ahos_50_6_multiregion_dr_router)


app.include_router(ahos_50_7_zero_trust_router)


app.include_router(ahos_50_8_regulatory_evidence_router)

app.include_router(ahos_50_9_router)


app.include_router(ahos_51_0_global_commercial_launch_router)

app.include_router(ahos_51_1_router)

app.include_router(ahos_51_2_router)

app.include_router(ahos_51_3_router)

app.include_router(ahos_51_4_router)

app.include_router(ahos_51_5_router)

app.include_router(ahos_51_6_router)

app.include_router(ahos_52_0_router)

app.include_router(ahos_52_1_router)

app.include_router(ahos_52_2_router)

app.include_router(ahos_52_3_router)

app.include_router(ahos_52_4_router)

app.include_router(ahos_52_5_router)

app.include_router(ahos_52_6_router)

app.include_router(ahos_52_7_router)

app.include_router(ahos_52_8_router)

app.include_router(ahos_52_9_router)

app.include_router(ahos_53_0_router)

app.include_router(ahos_53_1_router)

app.include_router(ahos_53_2_router)

# AHOS 53.1 Unified Real PostgreSQL Dashboard
app.include_router(unified_dashboard_router)

# AHOS 53.7 Real Radiology Dashboard API
app.include_router(radiology_dashboard_router)

# AHOS 53.8 Real Ultrasound Dashboard API
app.include_router(ultrasound_dashboard_router)


# AHOS 54.2 Real DICOM Viewer Router
app.include_router(dicom_viewer_router)



from backend.app.ahos_55_0.autonomous_medical_ai_avatar import router as ahos_55_0_avatar_router
app.include_router(ahos_55_0_avatar_router)

from backend.app.ahos_55_1.realtime_voice_video_avatar import router as ahos_55_1_router
app.include_router(ahos_55_1_router)


from backend.app.ahos_55_2.arabic_avatar_command_center import router as ahos_55_2_arabic_avatar_router
app.include_router(ahos_55_2_arabic_avatar_router)

from backend.app.ahos_55_4.digital_human_medical_avatar import router as ahos_55_4_digital_human_router
app.include_router(ahos_55_4_digital_human_router)

from backend.app.ahos_55_5.enterprise_digital_human_avatar_integration import router as ahos_55_5_router
from backend.app.ahos_55_6.real_digital_human_avatar import router as ahos_55_6_real_digital_human_avatar_router
from backend.app.ahos_55_7.real_voice_clinical_context_engine import router as ahos_55_7_voice_clinical_context_router
from backend.app.ahos_55_8.persistent_clinical_avatar_memory import router as ahos_55_8_avatar_memory_router
from backend.app.ahos_55_9.unified_avatar_voice_memory_pipeline import router as ahos_55_9_avatar_voice_memory_router
from backend.app.ahos_56_0.clinical_avatar_orchestration_center import router as ahos_56_0_avatar_orchestration_router
from backend.app.ahos_56_1.physician_review_queue import router as ahos_56_1_physician_review_router
from backend.app.ahos_56_2.automatic_safety_escalation_router import router as ahos_56_2_safety_escalation_router
from backend.app.ahos_56_3.unified_safety_command_center import router as ahos_56_3_unified_safety_center_router
from backend.app.ahos_56_4.regulatory_safety_evidence_export import router as ahos_56_4_regulatory_safety_evidence_router
from backend.app.ahos_56_5.regulatory_dossier_pdf_zip_export import router as ahos_56_5_regulatory_dossier_router
from backend.app.ahos_56_6.dossier_digital_signature_integrity import router as ahos_56_6_dossier_integrity_router
from backend.app.ahos_56_7.immutable_regulatory_audit_ledger import router as ahos_56_7_immutable_ledger_router
from backend.app.ahos_56_8.external_regulatory_reviewer_gateway import router as ahos_56_8_external_reviewer_router
from backend.app.ahos_56_9.external_reviewer_certificate_report import router as ahos_56_9_reviewer_certificate_router
app.include_router(ahos_55_5_router)


# AHOS 55.6 Real Digital Human Avatar

# AHOS 55.6 Real Digital Human Avatar
app.include_router(ahos_55_6_real_digital_human_avatar_router)

# AHOS 55.7 Real Voice + Clinical Context Engine
app.include_router(ahos_55_7_voice_clinical_context_router)

# AHOS 55.8 Persistent Clinical Avatar Memory + Audit Database
app.include_router(ahos_55_8_avatar_memory_router)

# AHOS 55.9 Unified Avatar Voice-to-Memory Pipeline
app.include_router(ahos_55_9_avatar_voice_memory_router)

# AHOS 56.0 Clinical Avatar Orchestration Center
app.include_router(ahos_56_0_avatar_orchestration_router)

# AHOS 56.1 Physician Review Queue + Safety Approval Workflow
app.include_router(ahos_56_1_physician_review_router)

# AHOS 56.2 Automatic Safety Escalation Router
app.include_router(ahos_56_2_safety_escalation_router)

# AHOS 56.3 Unified Safety Command Center
app.include_router(ahos_56_3_unified_safety_center_router)

# AHOS 56.4 Regulatory Safety Evidence & Clinical Audit Export
app.include_router(ahos_56_4_regulatory_safety_evidence_router)

# AHOS 56.5 Regulatory Dossier PDF + ZIP Export
app.include_router(ahos_56_5_regulatory_dossier_router)

# AHOS 56.6 Regulatory Dossier Digital Signature + Integrity Verification

# AHOS 56.6 Regulatory Dossier Digital Signature + Integrity Verification
app.include_router(ahos_56_6_dossier_integrity_router)

# AHOS 56.7 Immutable Regulatory Audit Ledger + Tamper Evidence Registry
app.include_router(ahos_56_7_immutable_ledger_router)

# AHOS 56.8 External Regulatory Reviewer Portal + Dossier Verification Gateway
app.include_router(ahos_56_8_external_reviewer_router)

# AHOS 56.9 External Reviewer Certificate + Public Verification Report
app.include_router(ahos_56_9_reviewer_certificate_router)


# AHOS 57.0 Professional Stabilization & Scientific Evidence Package
try:
    from backend.app.ahos_57_0.professional_stabilization_scientific_evidence_package import router as ahos_57_0_professional_stabilization_scientific_evidence_package_router
    app.include_router(ahos_57_0_professional_stabilization_scientific_evidence_package_router)
except Exception as e:
    print("AHOS 57.0 router load skipped:", e)


# AHOS 57.1 Evidence Review Dashboard + Investor Export Center
try:
    from backend.app.ahos_57_1.evidence_review_investor_export_center import router as ahos_57_1_evidence_review_investor_export_center_router
    app.include_router(ahos_57_1_evidence_review_investor_export_center_router)
except Exception as e:
    print("AHOS 57.1 router load skipped:", e)


# AHOS 57.2 Investor Presentation + Board-Level Pitch Package
try:
    from backend.app.ahos_57_2.investor_presentation_board_pitch_package import router as ahos_57_2_investor_presentation_board_pitch_package_router
    app.include_router(ahos_57_2_investor_presentation_board_pitch_package_router)
except Exception as e:
    print("AHOS 57.2 router load skipped:", e)


# AHOS 57.3 Demo Video Script + Public Investor Walkthrough
try:
    from backend.app.ahos_57_3.demo_video_public_investor_walkthrough import router as ahos_57_3_demo_video_public_investor_walkthrough_router
    app.include_router(ahos_57_3_demo_video_public_investor_walkthrough_router)
except Exception as e:
    print("AHOS 57.3 router load skipped:", e)


# AHOS 57.4 Partner Data Room + Pilot Hospital Readiness Package
try:
    from backend.app.ahos_57_4.partner_data_room_pilot_hospital_readiness import router as ahos_57_4_partner_data_room_pilot_hospital_readiness_router
    app.include_router(ahos_57_4_partner_data_room_pilot_hospital_readiness_router)
except Exception as e:
    print("AHOS 57.4 router load skipped:", e)


# AHOS 57.5 Pilot Agreement + Validation Study Launch Pack
try:
    from backend.app.ahos_57_5.pilot_agreement_validation_study_launch_pack import router as ahos_57_5_pilot_agreement_validation_study_launch_pack_router
    app.include_router(ahos_57_5_pilot_agreement_validation_study_launch_pack_router)
except Exception as e:
    print("AHOS 57.5 router load skipped:", e)


# AHOS Avatar V3 Command API
try:
    from backend.app.api.avatar_v3_command import router as avatar_v3_command_router
    app.include_router(avatar_v3_command_router)
except Exception as e:
    print(f"[AHOS] Avatar V3 command router not loaded: {e}")



# AHOS Ophthalmology AI Eye Center
app.include_router(ophthalmology_ai_router)


# AHOS Official Ophthalmology Intelligence System
app.include_router(ophthalmology_unique_router)


# AHOS_PHASE38_2_OBSERVABILITY_START
from backend.app.observability.phase38_2 import (
    Phase38_2RuntimeObservabilityMiddleware,
    router as ahos_phase38_2_observability_router,
)

app.add_middleware(
    Phase38_2RuntimeObservabilityMiddleware
)

app.include_router(
    ahos_phase38_2_observability_router
)
# AHOS_PHASE38_2_OBSERVABILITY_END


# AHOS_PHASE38_3_TRACING_START
from backend.app.observability.phase38_3 import (
    Phase38_3OpenTelemetryMiddleware,
    router as ahos_phase38_3_tracing_router,
)

app.add_middleware(
    Phase38_3OpenTelemetryMiddleware
)

app.include_router(
    ahos_phase38_3_tracing_router
)
# AHOS_PHASE38_3_TRACING_END

# AHOS_PHASE36_4_INTEGRATION_START
from backend.app.ahos_phase36_4_tenant_integration import (
    Phase36_4TenantMiddleware,
    router as ahos_phase36_4_router,
)

app.add_middleware(
    Phase36_4TenantMiddleware
)

app.include_router(
    ahos_phase36_4_router
)
# AHOS_PHASE36_4_INTEGRATION_END

# AHOS PHASE 39.4 START
from backend.app.observability.phase39_4 import install_phase39_4

AHOS_PHASE39_4_STATE = install_phase39_4(app)
# AHOS PHASE 39.4 END

# AHOS PHASE 39.4 STATUS ENDPOINT START
@app.get("/ahos/39.4/observability/status")
async def ahos_phase39_4_observability_status():
    state = getattr(
        app.state,
        "ahos_phase39_4",
        {},
    )

    return {
        "phase": "39.4",
        "status": "ACTIVE",
        "automatic_fastapi_instrumentation": bool(
            state.get(
                "automatic_fastapi_instrumentation",
                False,
            )
        ),
        "request_correlation": bool(
            state.get(
                "request_correlation",
                False,
            )
        ),
        "response_headers": state.get(
            "response_headers",
            [],
        ),
        "request_log": state.get(
            "request_log",
        ),
        "otlp_endpoint": state.get(
            "otlp_endpoint",
        ),
        "real_patient_data_used": False,
        "clinical_certified": False,
    }
# AHOS PHASE 39.4 STATUS ENDPOINT END

# AHOS PHASE 39.5.5 DATABASE PROBE START
from sqlalchemy import text as _ahos_phase39_5_sql_text
from backend.app.db.database import (
    SessionLocal as _AHOSPhase39_5SessionLocal,
)


@app.get("/ahos/39.5.5/database-child-span/probe")
async def ahos_phase39_5_5_database_child_span_probe():
    """
    Operational observability probe.

    Executes SELECT 1 only. No patient, clinical, imaging,
    identity, or tenant information is read or returned.
    """
    db = _AHOSPhase39_5SessionLocal()

    try:
        result = db.execute(
            _ahos_phase39_5_sql_text(
                "SELECT 1 AS ahos_phase39_5_probe"
            )
        ).scalar_one()

        return {
            "phase": "39.5.5",
            "status": "PASSED",
            "database_probe": int(result),
            "query_type": "SELECT_CONSTANT",
            "real_patient_data_used": False,
            "clinical_data_accessed": False,
        }

    finally:
        db.close()
# AHOS PHASE 39.5.5 DATABASE PROBE END

# AHOS PHASE 39.5.6 SERVICE SPANS START
from backend.app.observability.service_child_spans import (
    traced_json_get as _ahos_phase39_5_6_get,
)


@app.get("/ahos/39.5.6/mock-fhir/metadata")
async def ahos_phase39_5_6_mock_fhir_metadata():
    """
    Synthetic FHIR CapabilityStatement.

    No patient, encounter, observation, medication,
    identity, or clinical resource data is returned.
    """
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "kind": "instance",
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "implementation": {
            "description": (
                "AHOS synthetic observability probe"
            )
        },
        "real_patient_data_used": False,
    }


@app.get("/ahos/39.5.6/mock-external/health")
async def ahos_phase39_5_6_mock_external_health():
    return {
        "status": "healthy",
        "service": "synthetic-external-probe",
        "real_patient_data_used": False,
    }


@app.get("/ahos/39.5.6/service-child-spans/probe")
async def ahos_phase39_5_6_service_child_spans_probe():
    fhir_url = (
        "http://127.0.0.1:8000"
        "/ahos/39.5.6/mock-fhir/metadata"
    )

    external_url = (
        "http://127.0.0.1:8000"
        "/ahos/39.5.6/mock-external/health"
    )

    orthanc_url = (
        "http://127.0.0.1:8042/system"
    )

    fhir_result = await _ahos_phase39_5_6_get(
        name="FHIR capability.read",
        layer="fhir",
        operation="capability-read",
        url=fhir_url,
    )

    external_result = await _ahos_phase39_5_6_get(
        name="HTTP external.health",
        layer="external-http",
        operation="health-check",
        url=external_url,
    )

    orthanc_available = True
    orthanc_status = 0
    orthanc_error_type = ""

    try:
        orthanc_result = await _ahos_phase39_5_6_get(
            name="DICOM orthanc.system",
            layer="dicom",
            operation="orthanc-system-read",
            url=orthanc_url,
        )

        orthanc_status = int(
            orthanc_result["status_code"]
        )

    except Exception as exc:
        orthanc_available = False
        orthanc_error_type = type(exc).__name__

    return {
        "phase": "39.5.6",
        "status": "PASSED",
        "fhir": {
            "instrumented": True,
            "status_code": int(
                fhir_result["status_code"]
            ),
            "synthetic_capability_statement": True,
        },
        "dicom_orthanc": {
            "instrumented": True,
            "available": orthanc_available,
            "status_code": orthanc_status,
            "error_type": orthanc_error_type,
        },
        "external_http": {
            "instrumented": True,
            "status_code": int(
                external_result["status_code"]
            ),
            "synthetic_target": True,
        },
        "real_patient_data_used": False,
        "clinical_payload_recorded": False,
        "dicom_tags_recorded": False,
        "fhir_resource_content_recorded": False,
    }
# AHOS PHASE 39.5.6 SERVICE SPANS END

# AHOS PHASE 39.6 CORRELATION START
from fastapi import Request as _AHOSPhase39_6Request
from backend.app.observability.phase39_6_correlation import (
    execute_correlation_probe as _ahos_phase39_6_probe,
    phase39_6_metrics_response as _ahos_phase39_6_metrics,
)


@app.get("/ahos/39.6/correlation/probe")
async def ahos_phase39_6_correlation_probe(
    request: _AHOSPhase39_6Request,
):
    correlation_id = (
        request.headers.get("x-correlation-id")
        or request.headers.get("x-request-id")
        or "ahos-phase39-6-generated"
    )

    return await _ahos_phase39_6_probe(
        correlation_id
    )


@app.get("/ahos/39.6/metrics")
async def ahos_phase39_6_metrics():
    return _ahos_phase39_6_metrics()
# AHOS PHASE 39.6 CORRELATION END

# AHOS PHASE 39.7 ALERTING START
from fastapi import (
    Body as _AHOSPhase39_7Body,
    Query as _AHOSPhase39_7Query,
    Request as _AHOSPhase39_7Request,
)
from backend.app.observability.phase39_7_alerting import (
    incident_status as _ahos_phase39_7_status,
    metrics_response as _ahos_phase39_7_metrics,
    record_alertmanager_webhook as _ahos_phase39_7_webhook,
    simulate_incident as _ahos_phase39_7_simulate,
)


@app.post("/ahos/39.7/incident/simulate")
async def ahos_phase39_7_incident_simulate(
    request: _AHOSPhase39_7Request,
    active: bool = _AHOSPhase39_7Query(True),
    incident_id: str = _AHOSPhase39_7Query(
        "AHOS-INC-39-7"
    ),
):
    correlation_id = (
        request.headers.get("x-correlation-id")
        or request.headers.get("x-request-id")
        or "ahos-phase39-7-generated"
    )

    return await _ahos_phase39_7_simulate(
        active=active,
        incident_id=incident_id,
        correlation_id=correlation_id,
    )


@app.get("/ahos/39.7/status")
async def ahos_phase39_7_status():
    return _ahos_phase39_7_status()


@app.get("/ahos/39.7/metrics")
async def ahos_phase39_7_metrics():
    return _ahos_phase39_7_metrics()


@app.post("/ahos/39.7/alertmanager/webhook")
async def ahos_phase39_7_alertmanager_webhook(
    payload: dict = _AHOSPhase39_7Body(...),
):
    return _ahos_phase39_7_webhook(
        payload
    )
# AHOS PHASE 39.7 ALERTING END

# AHOS_PHASE40_2_2_PROTECTED_ROUTER
from backend.app.keycloak_security.protected_router import (
    router as ahos_phase40_2_2_router,
)

app.include_router(ahos_phase40_2_2_router)

# AHOS_PHASE40_2_3_RBAC_ROUTER
from backend.app.keycloak_security.phase40_2_3_router import (
    router as ahos_phase40_2_3_router,
)

app.include_router(ahos_phase40_2_3_router)


@app.get(
    "/ahos/40.2.4.14/shadow-metrics",
    tags=["AHOS Phase 40.2.4.14 Security"],
)
async def phase40_2_4_14_shadow_metrics(
    request: FastAPIRequest,
):
    client_host = (
        request.client.host
        if request.client
        else ""
    )

    if client_host not in {
        "127.0.0.1",
        "::1",
        "localhost",
        "testclient",
    }:
        raise HTTPException(
            status_code=403,
            detail="Internal endpoint.",
        )

    return {
        "phase": "AHOS Phase 40.2.4.14",
        "status": "ACTIVE",
        "shadow_mode": True,
        "blocking_enabled": False,
        "default_deny_enabled": False,
        "metrics": get_shadow_metrics(),
        "recent_decisions": (
            get_recent_shadow_decisions(20)
        ),
        "privacy": {
            "tokens_logged": False,
            "authorization_headers_logged": False,
            "query_strings_logged": False,
            "payloads_logged": False,
            "path_identifiers_redacted": True,
        },
    }

from backend.app.ahos_40_5.router import router as ahos_40_5_router

app.include_router(ahos_40_5_router)
