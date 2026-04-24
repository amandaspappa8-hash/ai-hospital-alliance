import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useLocation, Link } from "react-router-dom";
import { useTheme } from "@/lib/theme";
import RealtimePanel from "./RealtimePanel";
import PWAStatus from "./PWAStatus";
import { getUser } from "@/lib/auth-storage";
const ROUTE_LABELS = {
    "/dashboard": "Dashboard",
    "/overview": "Overview",
    "/patients": "Patients",
    "/doctors": "Doctors",
    "/appointments": "Appointments",
    "/reports": "Reports",
    "/nursing": "Nursing Workflow",
    "/radiology": "Radiology — AI Imaging",
    "/radiology/imaging": "Imaging Orders",
    "/radiology/pacs": "PACS Viewer",
    "/radiology/ct-mri": "CT / MRI Studies",
    "/labs": "Laboratory — AI Interpreter",
    "/labs/orders": "Lab Orders",
    "/labs/catalog": "Test Catalog",
    "/pharmacy": "Smart Pharmacy — FDA Global",
    "/pharmacy/medications": "Medications",
    "/pharmacy/interactions": "Drug Interactions",
    "/pharmacy/formulary": "Drug Formulary",
    "/pharmacy/discharge": "Discharge Counseling",
    "/pharmacy/prescriptions": "Prescriptions",
    "/specialties": "Specialties",
    "/specialties/cardiology": "Cardiology",
    "/specialties/neurology": "Neurology",
    "/specialties/emergency": "Emergency",
    "/specialties/icu": "ICU",
    "/specialties/pediatrics": "Pediatrics",
    "/ai-routing": "AI Engine",
    "/ai/clinical": "Clinical Decision AI",
    "/files": "File Manager",
    "/settings": "Settings",
    "/admin": "Admin Overview",
};
export default function Topbar() {
    const { pathname } = useLocation();
    const { theme, toggle } = useTheme();
    const user = getUser();
    const label = Object.entries(ROUTE_LABELS)
        .sort((a, b) => b[0].length - a[0].length)
        .find(([k]) => pathname.startsWith(k))?.[1] ?? "AI Hospital Alliance";
    const isDark = theme === "dark";
    return (_jsxs("header", { style: {
            height: 54,
            display: "flex", alignItems: "center",
            justifyContent: "space-between",
            padding: "0 24px",
            background: isDark ? "rgba(6,13,31,0.97)" : "rgba(248,250,252,0.97)",
            borderBottom: `1px solid ${isDark ? "rgba(59,130,246,0.12)" : "rgba(0,0,0,0.08)"}`,
            backdropFilter: "blur(16px)",
            position: "sticky", top: 0, zIndex: 100,
            gap: 12,
        }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10 }, children: [_jsx("div", { style: { fontSize: 11, fontWeight: 700, color: "#3b82f6", letterSpacing: 1 }, children: "\u25C8" }), _jsx("div", { style: { fontSize: 13, fontWeight: 700, color: isDark ? "white" : "#0f172a" }, children: label }), _jsx(PWAStatus, {})] }), _jsxs("div", { style: { display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("button", { onClick: toggle, style: {
                            width: 36, height: 36, borderRadius: 9, border: "none",
                            background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)",
                            color: isDark ? "#fbbf24" : "#6366f1",
                            cursor: "pointer", fontSize: 16,
                            display: "flex", alignItems: "center", justifyContent: "center",
                            transition: "all 0.2s",
                        }, title: isDark ? "Light mode" : "Dark mode", children: isDark ? "☀️" : "🌙" }), _jsx(RealtimePanel, {}), _jsxs("div", { style: {
                            display: "flex", alignItems: "center", gap: 8,
                            padding: "5px 12px", borderRadius: 10,
                            background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.04)",
                            border: `1px solid ${isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)"}`,
                        }, children: [_jsx("div", { style: {
                                    width: 26, height: 26, borderRadius: 7,
                                    background: "linear-gradient(135deg,#2563eb,#7c3aed)",
                                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13,
                                }, children: "\uD83D\uDC64" }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 11, fontWeight: 700, color: isDark ? "white" : "#0f172a", lineHeight: 1.2 }, children: user?.name?.split(" ")[0] ?? "User" }), _jsx("div", { style: { fontSize: 9, color: "#3b82f6", fontWeight: 700 }, children: user?.role })] })] }), _jsx(Link, { to: "/logout", style: {
                            width: 36, height: 36, borderRadius: 9,
                            background: "rgba(239,68,68,0.08)",
                            border: "1px solid rgba(239,68,68,0.2)",
                            color: "#f87171", fontSize: 15,
                            display: "flex", alignItems: "center", justifyContent: "center",
                            textDecoration: "none", transition: "all 0.2s",
                        }, title: "Logout", children: "\uD83D\uDEAA" })] })] }));
}
