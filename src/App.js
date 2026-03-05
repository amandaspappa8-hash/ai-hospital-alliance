import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Routes, Route, Navigate } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import OverviewPage from "./pages/OverviewPage";
import FileManager from "./pages/FileManager";
import PatientsPage from "./pages/PatientsPage";
import AppointmentsPage from "./pages/AppointmentsPage";
import ReportsPage from "./pages/ReportsPage";
import SettingsPage from "./pages/SettingsPage";
import PrescriptionsPage from "./pages/PrescriptionsPage";
import DrugFormularyPage from "./pages/DrugFormularyPage";
// صفحات سنبنيها (إذا لم تكن موجودة الآن: سننشئها بعد هذه الخطوة)
import LabOrdersPage from "./pages/LabOrdersPage";
import ImagingOrdersPage from "./pages/ImagingOrdersPage";
import CtMriPage from "./pages/CtMriPage";
import PacsPage from "./pages/PacsPage";
import MedicationsPage from "./pages/MedicationsPage";
import InteractionsPage from "./pages/InteractionsPage";
import NotesPage from "./pages/NotesPage";
export default function App() {
    return (_jsxs(Routes, { children: [_jsx(Route, { path: "/login", element: _jsx(Login, {}) }), _jsxs(Route, { path: "/", element: _jsx(AppLayout, {}), children: [_jsx(Route, { index: true, element: _jsx(Home, {}) }), _jsx(Route, { path: "overview", element: _jsx(OverviewPage, {}) }), _jsx(Route, { path: "dashboard", element: _jsx(Dashboard, {}) }), _jsx(Route, { path: "patients", element: _jsx(PatientsPage, {}) }), _jsx(Route, { path: "appointments", element: _jsx(AppointmentsPage, {}) }), _jsx(Route, { path: "notes", element: _jsx(NotesPage, {}) }), _jsx(Route, { path: "prescriptions", element: _jsx(PrescriptionsPage, {}) }), _jsx(Route, { path: "labs", element: _jsx(LabOrdersPage, {}) }), _jsx(Route, { path: "imaging", element: _jsx(ImagingOrdersPage, {}) }), _jsx(Route, { path: "ct-mri", element: _jsx(CtMriPage, {}) }), _jsx(Route, { path: "files", element: _jsx(FileManager, {}) }), _jsx(Route, { path: "reports", element: _jsx(ReportsPage, {}) }), _jsx(Route, { path: "pacs", element: _jsx(PacsPage, {}) }), _jsx(Route, { path: "formulary", element: _jsx(DrugFormularyPage, {}) }), _jsx(Route, { path: "medications", element: _jsx(MedicationsPage, {}) }), _jsx(Route, { path: "interactions", element: _jsx(InteractionsPage, {}) }), _jsx(Route, { path: "settings", element: _jsx(SettingsPage, {}) }), _jsx(Route, { path: "logout", element: _jsx(Navigate, { to: "/login", replace: true }) })] }), _jsx(Route, { path: "*", element: _jsx(Navigate, { to: "/", replace: true }) })] }));
}
