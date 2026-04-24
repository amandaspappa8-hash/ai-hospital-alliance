import { lazy, Suspense, ReactNode } from "react"
import { Routes, Route, Navigate } from "react-router-dom"
import ProtectedRoute from "@/components/auth/ProtectedRoute"
import AppLayout from "@/layouts/AppLayout"
import { useState } from "react"

const Login                = lazy(() => import("@/pages/Login"))
const LogoutPage           = lazy(() => import("@/pages/LogoutPage"))
const Home                 = lazy(() => import("@/pages/Home"))
const Dashboard            = lazy(() => import("@/pages/Dashboard"))
const OverviewPage         = lazy(() => import("@/pages/OverviewPage"))
const AdminOverviewPage    = lazy(() => import("@/pages/AdminOverviewPage"))
const PatientsPage         = lazy(() => import("@/pages/PatientsPage"))
const PatientProfilePage   = lazy(() => import("@/pages/PatientProfilePage"))
const DoctorsPage          = lazy(() => import("@/pages/DoctorsPage"))
const DoctorProfilePage    = lazy(() => import("@/pages/DoctorProfilePage"))
const AppointmentsPage     = lazy(() => import("@/pages/AppointmentsPage"))
const ReportsPage          = lazy(() => import("@/pages/ReportsPage"))
const NotesPage            = lazy(() => import("@/pages/NotesPage"))
const OrdersPage           = lazy(() => import("@/pages/OrdersPage"))
const NursesPage           = lazy(() => import("@/pages/NursesPage"))
const RadiologyPage        = lazy(() => import("@/pages/RadiologyPage"))
const ImagingOrdersPage    = lazy(() => import("@/pages/ImagingOrdersPage"))
const PacsPage             = lazy(() => import("@/pages/PacsPage"))
const CtMriPage            = lazy(() => import("@/pages/CtMriPage"))
const LabsPage             = lazy(() => import("@/pages/LabsPage"))
const LabPage              = lazy(() => import("@/pages/LabPage"))
const LabOrdersPage        = lazy(() => import("@/pages/LabOrdersPage"))
const LabCatalogPage       = lazy(() => import("@/pages/LabCatalogPage"))
const SmartPharmacyPage    = lazy(() => import("@/pages/SmartPharmacyPage"))
const MedicationsPage      = lazy(() => import("@/pages/MedicationsPage"))
const DrugFormularyPage    = lazy(() => import("@/pages/DrugFormularyPage"))
const InteractionsPage     = lazy(() => import("@/pages/InteractionsPage"))
const DischargeMedicationPage = lazy(() => import("@/pages/DischargeMedicationPage"))
const PrescriptionsPage    = lazy(() => import("@/pages/PrescriptionsPage"))
const SpecialtiesPage      = lazy(() => import("@/pages/SpecialtiesPage"))
const CardiologyPage       = lazy(() => import("@/pages/CardiologyPage"))
const NeurologyPage        = lazy(() => import("@/pages/NeurologyPage"))
const EmergencyPage        = lazy(() => import("@/pages/EmergencyPage"))
const ICUPage              = lazy(() => import("@/pages/ICUPage"))
const PediatricsPage       = lazy(() => import("@/pages/PediatricsPage"))
const AIRoutingPage        = lazy(() => import("@/pages/AIRoutingPage"))
const ClinicalDecisionPage = lazy(() => import("@/pages/ClinicalDecisionPage"))
const FileManager          = lazy(() => import("@/pages/FileManager"))
const SettingsPage         = lazy(() => import("@/pages/SettingsPage"))

function PageLoader() {
  return (
    <div style={{
      display: "flex", alignItems: "center", justifyContent: "center",
      height: "100vh", background: "#020817", color: "#64748b",
      fontFamily: "Inter, Arial, sans-serif", flexDirection: "column", gap: 14,
    }}>
      <div style={{
        width: 38, height: 38, border: "3px solid #1e3a5f",
        borderTop: "3px solid #3b82f6", borderRadius: "50%",
        animation: "spin 0.7s linear infinite",
      }} />
      <style>{"@keyframes spin{to{transform:rotate(360deg)}}"}</style>
      Loading...
    </div>
  )
}

function Protected({ children, routeKey }: { children: ReactNode; routeKey?: any }) {
  return (
    <ProtectedRoute routeKey={routeKey}>
      <AppLayout>{children}</AppLayout>
    </ProtectedRoute>
  )
}

export default function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/login"  element={<Login />} />
        <Route path="/logout" element={<LogoutPage />} />
        <Route path="/home"   element={<Home />} />
        <Route path="/"       element={<Navigate to="/dashboard" replace />} />

        <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
        <Route path="/overview"  element={<Protected routeKey="overview"><OverviewPage /></Protected>} />
        <Route path="/admin"     element={<Protected><AdminOverviewPage /></Protected>} />

        <Route path="/patients"          element={<Protected routeKey="patients"><PatientsPage /></Protected>} />
        <Route path="/patients/:id"      element={<Protected routeKey="patients"><PatientProfilePage /></Protected>} />
        <Route path="/notes"             element={<Protected routeKey="notes"><NotesPage /></Protected>} />
        <Route path="/notes/:patientId"  element={<Protected routeKey="notes"><NotesPage /></Protected>} />
        <Route path="/orders"            element={<Protected><OrdersPage /></Protected>} />
        <Route path="/orders/:patientId" element={<Protected><OrdersPage /></Protected>} />

        <Route path="/doctors"     element={<Protected><DoctorsPage /></Protected>} />
        <Route path="/doctors/:id" element={<Protected><DoctorProfilePage /></Protected>} />

        <Route path="/appointments" element={<Protected routeKey="appointments"><AppointmentsPage /></Protected>} />
        <Route path="/reports"      element={<Protected routeKey="reports"><ReportsPage /></Protected>} />
        <Route path="/nursing"      element={<Protected><NursesPage /></Protected>} />

        <Route path="/radiology"         element={<Protected><RadiologyPage /></Protected>} />
        <Route path="/radiology/imaging" element={<Protected><ImagingOrdersPage /></Protected>} />
        <Route path="/radiology/pacs"    element={<Protected><PacsPage /></Protected>} />
        <Route path="/radiology/ct-mri"  element={<Protected><CtMriPage /></Protected>} />
        <Route path="/pacs"              element={<Protected><PacsPage /></Protected>} />

        <Route path="/labs"            element={<Protected routeKey="labs"><LabsPage /></Protected>} />
        <Route path="/labs/orders"     element={<Protected><LabOrdersPage /></Protected>} />
        <Route path="/labs/catalog"    element={<Protected><LabCatalogPage /></Protected>} />
        <Route path="/labs/:patientId" element={<Protected routeKey="labs"><LabPage /></Protected>} />

        <Route path="/pharmacy"               element={<Protected routeKey="medications"><SmartPharmacyPage /></Protected>} />
        <Route path="/pharmacy/medications"   element={<Protected routeKey="medications"><MedicationsPage /></Protected>} />
        <Route path="/pharmacy/formulary"     element={<Protected routeKey="drug-formulary"><DrugFormularyPage /></Protected>} />
        <Route path="/pharmacy/interactions"  element={<Protected routeKey="interactions"><InteractionsPage /></Protected>} />
        <Route path="/pharmacy/discharge"     element={<Protected><DischargeMedicationPage /></Protected>} />
        <Route path="/pharmacy/prescriptions" element={<Protected><PrescriptionsPage /></Protected>} />
        <Route path="/medications"            element={<Protected routeKey="medications"><MedicationsPage /></Protected>} />

        <Route path="/specialties"            element={<Protected><SpecialtiesPage /></Protected>} />
        <Route path="/specialties/cardiology" element={<Protected><CardiologyPage /></Protected>} />
        <Route path="/specialties/neurology"  element={<Protected><NeurologyPage /></Protected>} />
        <Route path="/specialties/emergency"  element={<Protected><EmergencyPage /></Protected>} />
        <Route path="/specialties/icu"        element={<Protected><ICUPage /></Protected>} />
        <Route path="/specialties/pediatrics" element={<Protected><PediatricsPage /></Protected>} />

        <Route path="/ai-routing"  element={<Protected><AIRoutingPage /></Protected>} />
        <Route path="/ai"          element={<Protected><AIRoutingPage /></Protected>} />
        <Route path="/ai/clinical" element={<Protected><ClinicalDecisionPage /></Protected>} />

        <Route path="/files"    element={<Protected routeKey="file-manager"><FileManager /></Protected>} />
        <Route path="/settings" element={<Protected routeKey="settings"><SettingsPage /></Protected>} />

        <Route path="*" element={
          <div style={{ display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center", height:"100vh", background:"#020817", color:"white", fontFamily:"Inter,sans-serif" }}>
            <div style={{ fontSize:64, fontWeight:900, color:"#1e3a5f" }}>404</div>
            <a href="/dashboard" style={{ color:"#3b82f6", marginTop:12 }}>← Dashboard</a>
          </div>
        } />
      </Routes>
    </Suspense>
  )
}
