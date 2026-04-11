import PatientProfile from "./pages/PatientProfile";
import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Patients from "./pages/Patients";
import Pharmacy from "./pages/Pharmacy";
import Labs from "./pages/Labs";
import AIAssistant from "./pages/AIAssistant";
import Login from "./pages/Login";
import NurseWorkflow from "./pages/NurseWorkflow";

import AIDashboard from "./pages/AIDashboard";
import Radiology from "./pages/Radiology";
import PACS from "./pages/PACS";
import DoctorOrders from "./pages/DoctorOrders";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#f1f5f9" }}>
      <Sidebar />
      <main style={{ flex: 1, padding: 20 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
            path="/patients"
              <ProtectedRoute roles={["admin", "doctor", "nurse"]}>
                <Patients />
            path="/patients/:id"
                <PatientProfile />
            path="/pharmacy"
              <ProtectedRoute roles={["doctor", "admin"]}>
                <Pharmacy />
            path="/doctor-orders"
              <ProtectedRoute roles={["admin", "doctor"]}>
                <DoctorOrders />
            path="/nurse"
              <ProtectedRoute roles={["admin", "nurse"]}>
                <NurseWorkflow />
            path="/labs"
                <Labs />
            path="/ai"
                <AIAssistant />
        
<Route path="/ai-dashboard" element={<AIDashboard />} />
<Route path="/radiology" element={<Radiology />} />
<Route path="/pacs" element={<PACS />} />
</Routes>
      </main>
    </div>
  );
}
export default function App() {
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/*" element={<Layout />} />
      
    </AuthProvider>
