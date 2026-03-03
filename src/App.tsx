import { Routes, Route, Navigate } from "react-router-dom"
import AppLayout from "./layouts/AppLayout"

import Home from "./pages/Home"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import OverviewPage from "./pages/OverviewPage"
import FileManager from "./pages/FileManager"

import PatientsPage from "./pages/PatientsPage"
import AppointmentsPage from "./pages/AppointmentsPage"
import ReportsPage from "./pages/ReportsPage"
import SettingsPage from "./pages/SettingsPage"
import PrescriptionsPage from "./pages/PrescriptionsPage"
import DrugFormularyPage from "./pages/DrugFormularyPage"

// صفحات سنبنيها (إذا لم تكن موجودة الآن: سننشئها بعد هذه الخطوة)
import LabOrdersPage from "./pages/LabOrdersPage"
import ImagingOrdersPage from "./pages/ImagingOrdersPage"
import CtMriPage from "./pages/CtMriPage"
import PacsPage from "./pages/PacsPage"
import MedicationsPage from "./pages/MedicationsPage"
import InteractionsPage from "./pages/InteractionsPage"
import NotesPage from "./pages/NotesPage"

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<Login />} />

      {/* Protected/Inside Layout */}
      <Route path="/" element={<AppLayout />}>
        <Route index element={<Home />} />

        {/* Workspace */}
        <Route path="overview" element={<OverviewPage />} />
        <Route path="dashboard" element={<Dashboard />} />

        {/* Clinical */}
        <Route path="patients" element={<PatientsPage />} />
        <Route path="appointments" element={<AppointmentsPage />} />
        <Route path="notes" element={<NotesPage />} />

        {/* Orders */}
        <Route path="prescriptions" element={<PrescriptionsPage />} />
        <Route path="labs" element={<LabOrdersPage />} />
        <Route path="imaging" element={<ImagingOrdersPage />} />
        <Route path="ct-mri" element={<CtMriPage />} />

        {/* Documents */}
        <Route path="files" element={<FileManager />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="pacs" element={<PacsPage />} />

        {/* Pharmacy */}
        <Route path="formulary" element={<DrugFormularyPage />} />
        <Route path="medications" element={<MedicationsPage />} />
        <Route path="interactions" element={<InteractionsPage />} />

        {/* System */}
        <Route path="settings" element={<SettingsPage />} />
        <Route path="logout" element={<Navigate to="/login" replace />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
