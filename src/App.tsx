import EnterpriseAvatarDashboardPage from "./pages/EnterpriseAvatarDashboardPage";
import DigitalHumanMedicalAvatarPage from "./pages/DigitalHumanMedicalAvatarPage";
import ArabicAvatarCommandCenterPage from "./pages/ArabicAvatarCommandCenterPage";
import RealtimeMedicalAvatarPage from "./pages/RealtimeMedicalAvatarPage";
import MedicalAIAvatarPage from "./pages/MedicalAIAvatarPage";
import AHOS260GlobalAutonomousHospitalBrain from "./pages/executive/AHOS26_0GlobalAutonomousHospitalBrain";
import AHOS259GlobalAICrisisCommandCenter from "./pages/executive/AHOS25_9GlobalAICrisisCommandCenter";
import AHOS258GlobalExecutiveSituationRoom from "./pages/executive/AHOS25_8GlobalExecutiveSituationRoom";
import AHOS257GlobalHospitalFederation3DMap from "./pages/executive/AHOS25_7GlobalHospitalFederation3DMap";
import AHOS256GlobalExecutiveNeuralNetwork from "./pages/executive/AHOS25_6GlobalExecutiveNeuralNetwork";
import AHOS255ExecutiveDigitalTwin3D from "./pages/executive/AHOS25_5ExecutiveDigitalTwin3D";
import GlobalExecutiveAICommandPlatformPage from "./pages/command/GlobalExecutiveAICommandPlatformPage";
import ExecutiveCommandDashboard from "./pages/production/ExecutiveCommandDashboard";
import FrontendProductionDashboards from "./pages/production/FrontendProductionDashboards";
import RegionalHealthcareIntelligencePage from "./pages/RegionalHealthcareIntelligencePage";
import AutonomousResourceOptimizerPage from "./pages/AutonomousResourceOptimizerPage";
import AHOSResourceForecastPage from "./pages/AHOSResourceForecastPage";
import { lazy, Suspense } from "react";
import { getAuthState } from "@/lib/auth-storage";
import { Routes, Route, Navigate } from "react-router-dom"

import AppSidebar from "@/components/app/AppSidebar"

import Dashboard from "@/pages/Dashboard"
import AHOSLoginGlass from "@/pages/AHOSLoginGlass"
import DashboardCinematic from "@/pages/DashboardCinematic";

import AdminOverviewPage from "@/pages/AdminOverviewPage"
import OverviewPage from "@/pages/OverviewPage"
import PatientsPage from "@/pages/PatientsPage"
import PatientProfilePage from "@/pages/PatientProfilePage"
import DoctorsPage from "@/pages/DoctorsPage"
import AppointmentsPage from "@/pages/AppointmentsPage"
import ReportsPage from "@/pages/ReportsPage"
import NotesPage from "@/pages/NotesPage"
import OrdersPage from "@/pages/OrdersPage"
import NursesPage from "@/pages/NursesPage"

import RadiologyPage from "@/pages/RadiologyPage"
import PacsPage from "@/pages/PacsPage"
import EnterprisePACSPage from "@/pages/EnterprisePACSPage"

import LabsPage from "@/pages/LabsPage"
import LabPage from "@/pages/LabPage"
import LabCatalogPage from "@/pages/LabCatalogPage"
import LabOrdersPage from "@/pages/LabOrdersPage"

import SmartPharmacyPage from "@/pages/SmartPharmacyPage"
import MedicationsPage from "@/pages/MedicationsPage"
import DrugFormularyPage from "@/pages/DrugFormularyPage"
import InteractionsPage from "@/pages/InteractionsPage"
import DischargeMedicationPage from "@/pages/DischargeMedicationPage"
import PrescriptionsPage from "@/pages/PrescriptionsPage"

import AIClinicalCenter from "@/pages/AIClinicalCenter"
import AIRoutingPage from "@/pages/AIRoutingPage"
import ClinicalDecisionPage from "@/pages/ClinicalDecisionPage"

import SpecialtiesPage from "@/pages/SpecialtiesPage"
import CardiologyPage from "@/pages/CardiologyPage"
import NeurologyPage from "@/pages/NeurologyPage"
import EmergencyPage from "@/pages/EmergencyPage"
import ICUPage from "@/pages/ICUPage"
import PediatricsPage from "@/pages/PediatricsPage"

import Login from "@/pages/Login"
import LogoutPage from "@/pages/LogoutPage"
import RegisterPage from "@/pages/RegisterPage"
import SettingsPage from "@/pages/SettingsPage"
import FileManager from "@/pages/FileManager"
import HospitalOperationsCenter from "./pages/operations/HospitalOperationsCenter"
import LiveBedManagementPage from "./pages/operations/LiveBedManagementPage"
import AutonomousPatientFlowPage from "./pages/operations/AutonomousPatientFlowPage"
import EmergencyCommandCenterPage from "./pages/operations/EmergencyCommandCenterPage"
import AutonomousICUIntelligencePage from "./pages/operations/AutonomousICUIntelligencePage"
import RadiologyOperationsCenterPage from "./pages/operations/RadiologyOperationsCenterPage"
import LaboratoryOperationsCenterPage from "./pages/operations/LaboratoryOperationsCenterPage"
import PharmacyOperationsCenterPage from "./pages/operations/PharmacyOperationsCenterPage"
import ExecutiveCommandCenterPage from "./pages/ExecutiveCommandCenterPage";
import FinancialOperationsCenterPage from "./pages/FinancialOperationsCenterPage";
import SupplyChainIntelligenceCenterPage from "./pages/SupplyChainIntelligenceCenterPage";
import HospitalDigitalTwinPage from "./pages/HospitalDigitalTwinPage";
import AutonomousHospitalBrainPage from "./pages/AutonomousHospitalBrainPage";
import UnifiedExecutiveCommandCenterPage from "./pages/UnifiedExecutiveCommandCenterPage";
const AIUltrasoundXPage = lazy(() => import("@/pages/AIUltrasoundXPage"));
const AIUltrasoundX36Page = lazy(() => import("@/pages/AIUltrasoundX36Page"));
const AIUltrasoundX402Page = lazy(() => import("@/pages/AIUltrasoundX402Page"));
const Radiology3DViewerPage = lazy(() => import("@/pages/Radiology3DViewerPage"));
const MedicalVolumeVTKPage = lazy(() => import("@/pages/MedicalVolumeVTKPage"));
const RealMedicalVolumePage = lazy(() => import("@/pages/RealMedicalVolumePage"));
const GMINCommandCenter = lazy(() => import("@/pages/GMINCommandCenter"));
const GlobalMedicalIntelligenceDashboard = lazy(() => import("@/pages/GlobalMedicalIntelligenceDashboard"));
import GlobalMultiHospitalFederationPage from "./pages/GlobalMultiHospitalFederationPage";
import GlobalDigitalTwinCommandNetworkPage from "./pages/GlobalDigitalTwinCommandNetworkPage";
import AGHOSCorePage from "./pages/AGHOSCorePage";
import ClinicalIntelligenceMeshPage from "./pages/ClinicalIntelligenceMeshPage";
import RealTimeEventMonitoringCenterPage from "./pages/RealTimeEventMonitoringCenterPage";
import UnifiedClinicalDataExchangeHubPage from "./pages/UnifiedClinicalDataExchangeHubPage";
import AHOS556RealDigitalHumanAvatarPage from "./pages/AHOS556RealDigitalHumanAvatarPage";
import AHOS557VoiceClinicalContextPage from "./pages/AHOS557VoiceClinicalContextPage";
import AHOS558AvatarMemoryAuditPage from "./pages/AHOS558AvatarMemoryAuditPage";
import AHOS559UnifiedAvatarPipelinePage from "./pages/AHOS559UnifiedAvatarPipelinePage";
import AHOS560AvatarOrchestrationPage from "./pages/AHOS560AvatarOrchestrationPage";
import AHOS561PhysicianReviewPage from "./pages/AHOS561PhysicianReviewPage";
import AHOS562SafetyEscalationPage from "./pages/AHOS562SafetyEscalationPage";
import AHOS563UnifiedSafetyCenterPage from "./pages/AHOS563UnifiedSafetyCenterPage";
import AHOS564RegulatorySafetyEvidencePage from "./pages/AHOS564RegulatorySafetyEvidencePage";
import AHOS565RegulatoryDossierPage from "./pages/AHOS565RegulatoryDossierPage";
import AHOS566DossierIntegrityPage from "./pages/AHOS566DossierIntegrityPage";
import AHOS567ImmutableAuditLedgerPage from "./pages/AHOS567ImmutableAuditLedgerPage";
import AHOS568ExternalReviewerPortalPage from "./pages/AHOS568ExternalReviewerPortalPage";
import AHOS569ReviewerCertificatePage from "./pages/AHOS569ReviewerCertificatePage";
import AHOS570ProfessionalStabilizationPage from "./pages/AHOS570ProfessionalStabilizationPage";
import AHOS571EvidenceReviewInvestorExportPage from "./pages/AHOS571EvidenceReviewInvestorExportPage";
import AHOS572InvestorPresentationPage from "./pages/AHOS572InvestorPresentationPage";
import AHOS573InvestorWalkthroughPage from "./pages/AHOS573InvestorWalkthroughPage";
import AHOS574PartnerDataRoomPage from "./pages/AHOS574PartnerDataRoomPage";
import AHOS575PilotValidationPage from "./pages/AHOS575PilotValidationPage";
import AvatarLabPage from "./pages/AvatarLabPage";
import AdvancedMedicalHologramPage from "./pages/AdvancedMedicalHologramPage";
import MedicalHologramV2Page from "./pages/MedicalHologramV2Page";
import MedicalHologramDocsPage from "./pages/MedicalHologramDocsPage";
import MedicalHologramV1Page from "./pages/MedicalHologramV1Page";
import MedicalHologramBasicPage from "./pages/MedicalHologramBasicPage";
import MedicalHologramV3Page from "./pages/MedicalHologramV3Page";
import OphthalmologyAIEyeCenter from "./pages/OphthalmologyAIEyeCenter";
import OphthalmologyOfficialPage from "./pages/OphthalmologyOfficialPage";
import OphthalmologyIntegrationStatus from "./pages/OphthalmologyIntegrationStatus";
import MedicalDepartmentsHub from "./pages/MedicalDepartmentsHub";
import OphthalmologyPhase3Page from "./pages/OphthalmologyPhase3Page";
import OphthalmologyPhase4Page from "./pages/OphthalmologyPhase4Page";
import OphthalmologyPhase8Page from "./pages/OphthalmologyPhase8Page";
import OphthalmologyPhase9Page from "./pages/OphthalmologyPhase9Page";
import OphthalmologyPhase11Page from "./pages/OphthalmologyPhase11Page";
import OphthalmologyPhase12Page from "./pages/OphthalmologyPhase12Page";
import OphthalmologyPhase13Page from "./pages/OphthalmologyPhase13Page";
import OphthalmologyPhase14Page from "./pages/OphthalmologyPhase14Page";
import OphthalmologyPhase15Page from "./pages/OphthalmologyPhase15Page";
import OphthalmologyPhase16Page from "./pages/OphthalmologyPhase16Page";
import OphthalmologyPhase17Page from "./pages/OphthalmologyPhase17Page";
import OphthalmologyPhase18Page from "./pages/OphthalmologyPhase18Page";
import OphthalmologyPhase19Page from "./pages/OphthalmologyPhase19Page";
import OphthalmologyPhase20Page from "./pages/OphthalmologyPhase20Page";
import OphthalmologyPhase21Page from "./pages/OphthalmologyPhase21Page";
import OphthalmologyPhase22Page from "./pages/OphthalmologyPhase22Page";
import OphthalmologyPhase23Page from "./pages/OphthalmologyPhase23Page";
import OphthalmologyPhase24Page from "./pages/OphthalmologyPhase24Page";
import OphthalmologyDashboardIntegrationPage from "./pages/OphthalmologyDashboardIntegrationPage";
const PatientDigitalTwinCenter = lazy(() => import("@/pages/PatientDigitalTwinCenter"));
const MedicalMemoryLiveDashboard = lazy(() => import("@/pages/MedicalMemoryLiveDashboard"));

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#020817" }}>
<AppSidebar />
      <main style={{ flex: 1, minWidth: 0 }}>
        {children}
      </main>
    </div>
  )
}

function Page({ children }: { children: React.ReactNode }) {
  return <Shell>{children}</Shell>
}



function ProtectedRoute({ children }: { children: React.ReactNode }) {

  const auth = getAuthState()

  if (!auth) {
    return <Navigate to="/ahos-login" replace />
  }

  return <>{children}</>

}


function App() {
  return (
    <Suspense fallback={<div style={{ padding: 32, color: 'white' }}>Loading AI Hospital Alliance...</div>}>
    <Routes>

      <Route path="/" element={<AHOSLoginGlass />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/logout" element={<LogoutPage />} />

      <Route path="/login" element={<AHOSLoginGlass />} />
      <Route path="/ahos-login" element={<AHOSLoginGlass />} />
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/cinematic-dashboard" element={<Page><DashboardCinematic /></Page>} />
      
      <Route path="/admin" element={<Page><AdminOverviewPage /></Page>} />

      <Route path="/patients" element={<Page><PatientsPage /></Page>} />
      <Route path="/patient-digital-twin" element={<PatientDigitalTwinCenter />} />
      <Route path="/patients/:id" element={<Page><PatientProfilePage /></Page>} />
      <Route path="/doctors" element={<Page><DoctorsPage /></Page>} />
      <Route path="/appointments" element={<Page><AppointmentsPage /></Page>} />
      <Route path="/orders" element={<Page><OrdersPage /></Page>} />
      <Route path="/reports" element={<Page><ReportsPage /></Page>} />
      <Route path="/notes" element={<Page><NotesPage /></Page>} />
      <Route path="/nursing" element={<Page><NursesPage /></Page>} />

      <Route path="/radiology" element={<Page><RadiologyPage /></Page>} />
      <Route path="/radiology-3d" element={<Page><Radiology3DViewerPage /></Page>} />
      <Route path="/medical-volume-vtk" element={<Page><MedicalVolumeVTKPage /></Page>} />
      <Route path="/real-medical-volume" element={<Page><RealMedicalVolumePage /></Page>} />
      <Route path="/pacs" element={<Page><PacsPage /></Page>} />
      <Route path="/enterprise-pacs" element={<Page><EnterprisePACSPage /></Page>} />

      <Route path="/labs" element={<Page><LabsPage /></Page>} />
      <Route path="/lab" element={<Page><LabPage /></Page>} />
      <Route path="/labs/catalog" element={<Page><LabCatalogPage /></Page>} />
      <Route path="/labs/orders" element={<Page><LabOrdersPage /></Page>} />

      <Route path="/pharmacy" element={<Page><SmartPharmacyPage /></Page>} />
      <Route path="/pharmacy/medications" element={<Page><MedicationsPage /></Page>} />
      <Route path="/pharmacy/formulary" element={<Page><DrugFormularyPage /></Page>} />
      <Route path="/pharmacy/interactions" element={<Page><InteractionsPage /></Page>} />
      <Route path="/pharmacy/discharge" element={<Page><DischargeMedicationPage /></Page>} />
      <Route path="/pharmacy/prescriptions" element={<Page><PrescriptionsPage /></Page>} />

      <Route path="/ai-clinical" element={<Page><AIClinicalCenter /></Page>} />
      <Route path="/ai-routing" element={<Page><AIRoutingPage /></Page>} />
      <Route path="/clinical-decision" element={<Page><ClinicalDecisionPage /></Page>} />

      <Route path="/medical-memory-live" element={<MedicalMemoryLiveDashboard />} />
      <Route path="/gmin" element={<GMINCommandCenter />} />
      <Route path="/gmin-dashboard" element={<Page><GlobalMedicalIntelligenceDashboard /></Page>} />

      <Route path="/specialties" element={<Page><SpecialtiesPage /></Page>} />
      <Route path="/specialties/cardiology" element={<Page><CardiologyPage /></Page>} />
      <Route path="/specialties/neurology" element={<Page><NeurologyPage /></Page>} />
      <Route path="/specialties/emergency" element={<Page><EmergencyPage /></Page>} />
      <Route path="/specialties/icu" element={<Page><ICUPage /></Page>} />
      <Route path="/specialties/pediatrics" element={<Page><PediatricsPage /></Page>} />

      <Route path="/ai-ultrasound-x" element={<Page><AIUltrasoundXPage /></Page>} />
      <Route path="/ai-ultrasound-x-3-6" element={<Page><AIUltrasoundX36Page /></Page>} />
      <Route path="/ai-ultrasound-x-4-0-2" element={<Page><AIUltrasoundX402Page /></Page>} />

      <Route path="/settings" element={<Page><SettingsPage /></Page>} />
      <Route path="/files" element={<Page><FileManager /></Page>} />

      <Route
        path="/ahos-25-9-crisis-command-center"
        element={<AHOS259GlobalAICrisisCommandCenter />}
      />

  <Route
    path="/ahos-26-0-autonomous-brain"
    element={<AHOS260GlobalAutonomousHospitalBrain />}
  />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
      <Route path="/ahos/resource-forecast" element={<AHOSResourceForecastPage />} />
  <Route path="/ahos/resource-optimizer" element={<AutonomousResourceOptimizerPage />} />
  <Route path="/ahos/regional-intelligence" element={<RegionalHealthcareIntelligencePage />} />
  <Route path="/production-dashboards" element={<FrontendProductionDashboards />} />
  <Route path="/executive-command-center" element={<ExecutiveCommandCenterPage />} />
  <Route path="/financial-operations-center" element={<FinancialOperationsCenterPage />} />
  <Route path="/supply-chain-intelligence-center" element={<SupplyChainIntelligenceCenterPage />} />
  <Route path="/hospital-digital-twin-center" element={<HospitalDigitalTwinPage />} />
  <Route path="/autonomous-hospital-brain" element={<AutonomousHospitalBrainPage />} />
  <Route path="/unified-executive-command-center" element={<UnifiedExecutiveCommandCenterPage />} />
  <Route path="/global-federation-dashboard" element={<GlobalMultiHospitalFederationPage />} />
  
  <Route
    path="/ahos-25-8-situation-room"
    element={<AHOS258GlobalExecutiveSituationRoom />}
  />

  <Route path="/ahos-25-7-global-federation-3d-map" element={<AHOS257GlobalHospitalFederation3DMap />} />
  <Route path="/ahos-25-6-neural-network" element={<AHOS256GlobalExecutiveNeuralNetwork />} />
  <Route path="/ahos-25-5-digital-twin-3d" element={<AHOS255ExecutiveDigitalTwin3D />} />
  <Route path="/global-executive-ai-command" element={<GlobalExecutiveAICommandPlatformPage />} />
  <Route path="/global-digital-twin-network" element={<GlobalDigitalTwinCommandNetworkPage />} />
  <Route path="/aghos-core" element={<AGHOSCorePage />} />
  <Route path="/clinical-intelligence-mesh" element={<ClinicalIntelligenceMeshPage />} />
  <Route path="/realtime-event-monitoring" element={<RealTimeEventMonitoringCenterPage />} />
  <Route path="/clinical-data-exchange-hub" element={<UnifiedClinicalDataExchangeHubPage />} />
  <Route path="/executive-command-dashboard" element={<ExecutiveCommandDashboard />} />

<Route
  path="/hospital-operations-center"
  element={<HospitalOperationsCenter />}
/>

<Route path="/live-bed-management" element={<LiveBedManagementPage />} />

<Route
  path="/autonomous-patient-flow"
  element={<AutonomousPatientFlowPage />}
/>

<Route
  path="/emergency-command-center"
  element={<EmergencyCommandCenterPage />}
/>

<Route
  path="/icu-intelligence-center"
  element={<AutonomousICUIntelligencePage />}
/>

<Route
  path="/radiology-operations-center"
  element={<RadiologyOperationsCenterPage />}
/>

<Route
  path="/laboratory-operations-center"
  element={<LaboratoryOperationsCenterPage />}
/>

<Route
  path="/pharmacy-operations-center"
  element={<PharmacyOperationsCenterPage />}
/>

  <Route path="/medical-ai-avatar" element={<MedicalAIAvatarPage />} />

  <Route path="/realtime-medical-avatar" element={<RealtimeMedicalAvatarPage />} />
  <Route path="/arabic-avatar-command" element={<ArabicAvatarCommandCenterPage />} />
  <Route path="/digital-human-avatar" element={<DigitalHumanMedicalAvatarPage />} />

<Route
 path="/enterprise-avatar-dashboard"
 element={<EnterpriseAvatarDashboardPage />}
/>

          <Route path="/ahos/55.6/real-digital-human-avatar" element={<AHOS556RealDigitalHumanAvatarPage />} />                  <Route path="/ahos/55.7/voice-clinical-context" element={<AHOS557VoiceClinicalContextPage />} />
                  <Route path="/ahos/55.8/avatar-memory-audit" element={<AHOS558AvatarMemoryAuditPage />} />
                  <Route path="/ahos/55.9/avatar-voice-memory-pipeline" element={<AHOS559UnifiedAvatarPipelinePage />} />
                  <Route path="/ahos/56.0/avatar-orchestration" element={<AHOS560AvatarOrchestrationPage />} />
                  <Route path="/ahos/56.1/physician-review" element={<AHOS561PhysicianReviewPage />} />
                          <Route path="/ahos/56.2/safety-escalation" element={<AHOS562SafetyEscalationPage />} />
                          <Route path="/ahos/56.3/unified-safety-center" element={<AHOS563UnifiedSafetyCenterPage />} />
                          <Route path="/ahos/56.4/regulatory-safety-evidence" element={<AHOS564RegulatorySafetyEvidencePage />} />
                          <Route path="/ahos/56.5/regulatory-dossier" element={<AHOS565RegulatoryDossierPage />} />
                          <Route path="/ahos/56.6/dossier-integrity" element={<AHOS566DossierIntegrityPage />} />
                          <Route path="/ahos/56.7/immutable-audit-ledger" element={<AHOS567ImmutableAuditLedgerPage />} />
                          <Route path="/ahos/56.8/external-reviewer" element={<AHOS568ExternalReviewerPortalPage />} />
                          <Route path="/ahos/56.9/reviewer-certificate" element={<AHOS569ReviewerCertificatePage />} />
          <Route path="/ahos/57.0/professional-stabilization" element={<AHOS570ProfessionalStabilizationPage />} />
          <Route path="/ahos/57.1/evidence-review-investor-export" element={<AHOS571EvidenceReviewInvestorExportPage />} />
          <Route path="/ahos/57.2/investor-presentation" element={<AHOS572InvestorPresentationPage />} />
          <Route path="/ahos/57.3/investor-walkthrough" element={<AHOS573InvestorWalkthroughPage />} />
          <Route path="/ahos/57.4/partner-data-room" element={<AHOS574PartnerDataRoomPage />} />
          <Route path="/ahos/57.5/pilot-validation" element={<AHOS575PilotValidationPage />} />
          <Route path="/avatar-lab" element={<AvatarLabPage />} />
          <Route path="/avatar-3d-hologram" element={<AdvancedMedicalHologramPage />} />
          <Route path="/avatar-medical-v2" element={<MedicalHologramV2Page />} />
          <Route path="/medical-hologram-docs" element={<MedicalHologramDocsPage />} />
          <Route path="/avatar-medical-v1" element={<MedicalHologramV1Page />} />
          <Route path="/avatar-medical-basic" element={<MedicalHologramBasicPage />} />
          <Route path="/avatar-medical-v3" element={<MedicalHologramV3Page />} />
          <Route path="/medical-hologram" element={<MedicalHologramV3Page />} />
                <Route path="/ophthalmology" element={<OphthalmologyAIEyeCenter />} />
              <Route path="/ophthalmology-ai-eye-center" element={<OphthalmologyAIEyeCenter />} />
              <Route path="/eye-center" element={<OphthalmologyAIEyeCenter />} />
              <Route path="/ophthalmology" element={<OphthalmologyOfficialPage />} />
              <Route path="/eye-center" element={<OphthalmologyOfficialPage />} />
              <Route path="/ahos-eye-center" element={<OphthalmologyOfficialPage />} />
              <Route path="/ophthalmology-integration" element={<OphthalmologyIntegrationStatus />} />
              <Route path="/medical-departments" element={<MedicalDepartmentsHub />} />
              <Route path="/ahos-main" element={<MedicalDepartmentsHub />} />
              <Route path="/departments" element={<MedicalDepartmentsHub />} />
              <Route path="/ophthalmology-phase-3" element={<OphthalmologyPhase3Page />} />
              <Route path="/ophthalmology-phase-4" element={<OphthalmologyPhase4Page />} />
              <Route path="/ophthalmology-phase-8" element={<OphthalmologyPhase8Page />} />
              <Route path="/ophthalmology-phase-9" element={<OphthalmologyPhase9Page />} />
              <Route path="/ophthalmology-phase-11" element={<OphthalmologyPhase11Page />} />
              <Route path="/ophthalmology-phase-12" element={<OphthalmologyPhase12Page />} />
              <Route path="/ophthalmology-phase-13" element={<OphthalmologyPhase13Page />} />
              <Route path="/ophthalmology-phase-14" element={<OphthalmologyPhase14Page />} />
              <Route path="/ophthalmology-phase-15" element={<OphthalmologyPhase15Page />} />
              <Route path="/ophthalmology-phase-16" element={<OphthalmologyPhase16Page />} />
              <Route path="/ophthalmology-phase-17" element={<OphthalmologyPhase17Page />} />
              <Route path="/ophthalmology-phase-18" element={<OphthalmologyPhase18Page />} />
              <Route path="/ophthalmology-phase-19" element={<OphthalmologyPhase19Page />} />
              <Route path="/ophthalmology-phase-20" element={<OphthalmologyPhase20Page />} />
              <Route path="/ophthalmology-phase-21" element={<OphthalmologyPhase21Page />} />
              <Route path="/ophthalmology-phase-22" element={<OphthalmologyPhase22Page />} />
              <Route path="/ophthalmology-phase-23" element={<OphthalmologyPhase23Page />} />
              <Route path="/ophthalmology-phase-24" element={<OphthalmologyPhase24Page />} />
              <Route path="/ophthalmology-dashboard-integration" element={<OphthalmologyDashboardIntegrationPage />} />
              <Route path="/ophthalmology-phase-25" element={<OphthalmologyDashboardIntegrationPage />} />
      </Routes>

    </Suspense>

  )
}

export default App;
