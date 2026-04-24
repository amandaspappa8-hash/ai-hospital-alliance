import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { lazy, Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import AppLayout from "@/layouts/AppLayout";
const Login = lazy(() => import("@/pages/Login"));
const LogoutPage = lazy(() => import("@/pages/LogoutPage"));
const Home = lazy(() => import("@/pages/Home"));
const Dashboard = lazy(() => import("@/pages/Dashboard"));
const OverviewPage = lazy(() => import("@/pages/OverviewPage"));
const AdminOverviewPage = lazy(() => import("@/pages/AdminOverviewPage"));
const PatientsPage = lazy(() => import("@/pages/PatientsPage"));
const PatientProfilePage = lazy(() => import("@/pages/PatientProfilePage"));
const DoctorsPage = lazy(() => import("@/pages/DoctorsPage"));
const DoctorProfilePage = lazy(() => import("@/pages/DoctorProfilePage"));
const AppointmentsPage = lazy(() => import("@/pages/AppointmentsPage"));
const ReportsPage = lazy(() => import("@/pages/ReportsPage"));
const NotesPage = lazy(() => import("@/pages/NotesPage"));
const OrdersPage = lazy(() => import("@/pages/OrdersPage"));
const NursesPage = lazy(() => import("@/pages/NursesPage"));
const RadiologyPage = lazy(() => import("@/pages/RadiologyPage"));
const ImagingOrdersPage = lazy(() => import("@/pages/ImagingOrdersPage"));
const PacsPage = lazy(() => import("@/pages/PacsPage"));
const CtMriPage = lazy(() => import("@/pages/CtMriPage"));
const LabsPage = lazy(() => import("@/pages/LabsPage"));
const LabPage = lazy(() => import("@/pages/LabPage"));
const LabOrdersPage = lazy(() => import("@/pages/LabOrdersPage"));
const LabCatalogPage = lazy(() => import("@/pages/LabCatalogPage"));
const SmartPharmacyPage = lazy(() => import("@/pages/SmartPharmacyPage"));
const MedicationsPage = lazy(() => import("@/pages/MedicationsPage"));
const DrugFormularyPage = lazy(() => import("@/pages/DrugFormularyPage"));
const InteractionsPage = lazy(() => import("@/pages/InteractionsPage"));
const DischargeMedicationPage = lazy(() => import("@/pages/DischargeMedicationPage"));
const PrescriptionsPage = lazy(() => import("@/pages/PrescriptionsPage"));
const SpecialtiesPage = lazy(() => import("@/pages/SpecialtiesPage"));
const CardiologyPage = lazy(() => import("@/pages/CardiologyPage"));
const NeurologyPage = lazy(() => import("@/pages/NeurologyPage"));
const EmergencyPage = lazy(() => import("@/pages/EmergencyPage"));
const ICUPage = lazy(() => import("@/pages/ICUPage"));
const PediatricsPage = lazy(() => import("@/pages/PediatricsPage"));
const AIRoutingPage = lazy(() => import("@/pages/AIRoutingPage"));
const ClinicalDecisionPage = lazy(() => import("@/pages/ClinicalDecisionPage"));
const FileManager = lazy(() => import("@/pages/FileManager"));
const SettingsPage = lazy(() => import("@/pages/SettingsPage"));
function PageLoader() {
    return (_jsxs("div", { style: {
            display: "flex", alignItems: "center", justifyContent: "center",
            height: "100vh", background: "#020817", color: "#64748b",
            fontFamily: "Inter, Arial, sans-serif", flexDirection: "column", gap: 14,
        }, children: [_jsx("div", { style: {
                    width: 38, height: 38, border: "3px solid #1e3a5f",
                    borderTop: "3px solid #3b82f6", borderRadius: "50%",
                    animation: "spin 0.7s linear infinite",
                } }), _jsx("style", { children: "@keyframes spin{to{transform:rotate(360deg)}}" }), "Loading..."] }));
}
function Protected({ children, routeKey }) {
    return (_jsx(ProtectedRoute, { routeKey: routeKey, children: _jsx(AppLayout, { children: children }) }));
}
export default function App() {
    return (_jsx(Suspense, { fallback: _jsx(PageLoader, {}), children: _jsxs(Routes, { children: [_jsx(Route, { path: "/login", element: _jsx(Login, {}) }), _jsx(Route, { path: "/logout", element: _jsx(LogoutPage, {}) }), _jsx(Route, { path: "/home", element: _jsx(Home, {}) }), _jsx(Route, { path: "/", element: _jsx(Navigate, { to: "/dashboard", replace: true }) }), _jsx(Route, { path: "/dashboard", element: _jsx(Protected, { children: _jsx(Dashboard, {}) }) }), _jsx(Route, { path: "/overview", element: _jsx(Protected, { routeKey: "overview", children: _jsx(OverviewPage, {}) }) }), _jsx(Route, { path: "/admin", element: _jsx(Protected, { children: _jsx(AdminOverviewPage, {}) }) }), _jsx(Route, { path: "/patients", element: _jsx(Protected, { routeKey: "patients", children: _jsx(PatientsPage, {}) }) }), _jsx(Route, { path: "/patients/:id", element: _jsx(Protected, { routeKey: "patients", children: _jsx(PatientProfilePage, {}) }) }), _jsx(Route, { path: "/notes", element: _jsx(Protected, { routeKey: "notes", children: _jsx(NotesPage, {}) }) }), _jsx(Route, { path: "/notes/:patientId", element: _jsx(Protected, { routeKey: "notes", children: _jsx(NotesPage, {}) }) }), _jsx(Route, { path: "/orders", element: _jsx(Protected, { children: _jsx(OrdersPage, {}) }) }), _jsx(Route, { path: "/orders/:patientId", element: _jsx(Protected, { children: _jsx(OrdersPage, {}) }) }), _jsx(Route, { path: "/doctors", element: _jsx(Protected, { children: _jsx(DoctorsPage, {}) }) }), _jsx(Route, { path: "/doctors/:id", element: _jsx(Protected, { children: _jsx(DoctorProfilePage, {}) }) }), _jsx(Route, { path: "/appointments", element: _jsx(Protected, { routeKey: "appointments", children: _jsx(AppointmentsPage, {}) }) }), _jsx(Route, { path: "/reports", element: _jsx(Protected, { routeKey: "reports", children: _jsx(ReportsPage, {}) }) }), _jsx(Route, { path: "/nursing", element: _jsx(Protected, { children: _jsx(NursesPage, {}) }) }), _jsx(Route, { path: "/radiology", element: _jsx(Protected, { children: _jsx(RadiologyPage, {}) }) }), _jsx(Route, { path: "/radiology/imaging", element: _jsx(Protected, { children: _jsx(ImagingOrdersPage, {}) }) }), _jsx(Route, { path: "/radiology/pacs", element: _jsx(Protected, { children: _jsx(PacsPage, {}) }) }), _jsx(Route, { path: "/radiology/ct-mri", element: _jsx(Protected, { children: _jsx(CtMriPage, {}) }) }), _jsx(Route, { path: "/pacs", element: _jsx(Protected, { children: _jsx(PacsPage, {}) }) }), _jsx(Route, { path: "/labs", element: _jsx(Protected, { routeKey: "labs", children: _jsx(LabsPage, {}) }) }), _jsx(Route, { path: "/labs/orders", element: _jsx(Protected, { children: _jsx(LabOrdersPage, {}) }) }), _jsx(Route, { path: "/labs/catalog", element: _jsx(Protected, { children: _jsx(LabCatalogPage, {}) }) }), _jsx(Route, { path: "/labs/:patientId", element: _jsx(Protected, { routeKey: "labs", children: _jsx(LabPage, {}) }) }), _jsx(Route, { path: "/pharmacy", element: _jsx(Protected, { routeKey: "medications", children: _jsx(SmartPharmacyPage, {}) }) }), _jsx(Route, { path: "/pharmacy/medications", element: _jsx(Protected, { routeKey: "medications", children: _jsx(MedicationsPage, {}) }) }), _jsx(Route, { path: "/pharmacy/formulary", element: _jsx(Protected, { routeKey: "drug-formulary", children: _jsx(DrugFormularyPage, {}) }) }), _jsx(Route, { path: "/pharmacy/interactions", element: _jsx(Protected, { routeKey: "interactions", children: _jsx(InteractionsPage, {}) }) }), _jsx(Route, { path: "/pharmacy/discharge", element: _jsx(Protected, { children: _jsx(DischargeMedicationPage, {}) }) }), _jsx(Route, { path: "/pharmacy/prescriptions", element: _jsx(Protected, { children: _jsx(PrescriptionsPage, {}) }) }), _jsx(Route, { path: "/medications", element: _jsx(Protected, { routeKey: "medications", children: _jsx(MedicationsPage, {}) }) }), _jsx(Route, { path: "/specialties", element: _jsx(Protected, { children: _jsx(SpecialtiesPage, {}) }) }), _jsx(Route, { path: "/specialties/cardiology", element: _jsx(Protected, { children: _jsx(CardiologyPage, {}) }) }), _jsx(Route, { path: "/specialties/neurology", element: _jsx(Protected, { children: _jsx(NeurologyPage, {}) }) }), _jsx(Route, { path: "/specialties/emergency", element: _jsx(Protected, { children: _jsx(EmergencyPage, {}) }) }), _jsx(Route, { path: "/specialties/icu", element: _jsx(Protected, { children: _jsx(ICUPage, {}) }) }), _jsx(Route, { path: "/specialties/pediatrics", element: _jsx(Protected, { children: _jsx(PediatricsPage, {}) }) }), _jsx(Route, { path: "/ai-routing", element: _jsx(Protected, { children: _jsx(AIRoutingPage, {}) }) }), _jsx(Route, { path: "/ai", element: _jsx(Protected, { children: _jsx(AIRoutingPage, {}) }) }), _jsx(Route, { path: "/ai/clinical", element: _jsx(Protected, { children: _jsx(ClinicalDecisionPage, {}) }) }), _jsx(Route, { path: "/files", element: _jsx(Protected, { routeKey: "file-manager", children: _jsx(FileManager, {}) }) }), _jsx(Route, { path: "/settings", element: _jsx(Protected, { routeKey: "settings", children: _jsx(SettingsPage, {}) }) }), _jsx(Route, { path: "*", element: _jsxs("div", { style: { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020817", color: "white", fontFamily: "Inter,sans-serif" }, children: [_jsx("div", { style: { fontSize: 64, fontWeight: 900, color: "#1e3a5f" }, children: "404" }), _jsx("a", { href: "/dashboard", style: { color: "#3b82f6", marginTop: 12 }, children: "\u2190 Dashboard" })] }) })] }) }));
}
