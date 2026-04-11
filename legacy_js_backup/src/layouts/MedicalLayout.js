import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { NavLink } from "react-router-dom";
import { LayoutDashboard, Users, ClipboardList, FileText, Stethoscope, Brain, Activity, } from "lucide-react";
export default function MedicalLayout({ children }) {
    return (_jsxs("div", { style: { display: "flex", height: "100vh", background: "#0b1220" }, children: [_jsxs("div", { style: {
                    width: 260,
                    background: "#111827",
                    borderRight: "1px solid #374151",
                    padding: 20,
                }, children: [_jsx("div", { style: {
                            fontSize: 20,
                            fontWeight: 700,
                            marginBottom: 30,
                            color: "white",
                        }, children: "AI Hospital" }), _jsx(Nav, { icon: _jsx(LayoutDashboard, { size: 18 }), to: "/dashboard", label: "Dashboard" }), _jsx(Nav, { icon: _jsx(Brain, { size: 18 }), to: "/ai-routing", label: "AI Routing" }), _jsx(Nav, { icon: _jsx(Users, { size: 18 }), to: "/patients", label: "Patients" }), _jsx(Nav, { icon: _jsx(ClipboardList, { size: 18 }), to: "/orders", label: "Orders" }), _jsx(Nav, { icon: _jsx(FileText, { size: 18 }), to: "/reports", label: "Reports" }), _jsx(Nav, { icon: _jsx(Stethoscope, { size: 18 }), to: "/appointments", label: "Appointments" }), _jsx(Nav, { icon: _jsx(Activity, { size: 18 }), to: "/notes", label: "Notes" })] }), _jsx("div", { style: { flex: 1, overflow: "auto" }, children: children })] }));
}
function Nav({ icon, to, label, }) {
    return (_jsxs(NavLink, { to: to, style: ({ isActive }) => ({
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "12px",
            borderRadius: 10,
            marginBottom: 8,
            textDecoration: "none",
            color: isActive ? "#22c55e" : "#cbd5e1",
            background: isActive ? "#0b1220" : "transparent",
        }), children: [icon, label] }));
}
