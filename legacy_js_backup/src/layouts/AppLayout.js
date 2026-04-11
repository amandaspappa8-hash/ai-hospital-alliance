import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import AppSidebar from "@/components/app/AppSidebar";
import { Outlet, useLocation } from "react-router-dom";
import { getUser } from "@/lib/auth-storage";
function getPageTitle(pathname) {
    if (pathname.startsWith("/dashboard"))
        return "Dashboard";
    if (pathname.startsWith("/ai-routing"))
        return "AI Clinical Routing";
    if (pathname.startsWith("/orders"))
        return "Clinical Orders";
    if (pathname.startsWith("/patients"))
        return "Patients";
    if (pathname.startsWith("/patient-profile"))
        return "Patient Profile";
    if (pathname.startsWith("/appointments"))
        return "Appointments";
    if (pathname.startsWith("/reports"))
        return "Reports";
    if (pathname.startsWith("/notes"))
        return "Clinical Notes";
    if (pathname.startsWith("/pacs"))
        return "PACS";
    return "AI Hospital Alliance";
}
function getPageSubtitle(pathname) {
    if (pathname.startsWith("/dashboard"))
        return "Hospital overview and operational metrics";
    if (pathname.startsWith("/ai-routing"))
        return "AI-supported triage and routing";
    if (pathname.startsWith("/orders"))
        return "Labs, imaging, pharmacy, and referrals";
    if (pathname.startsWith("/patients"))
        return "Electronic medical record workspace";
    if (pathname.startsWith("/patient-profile"))
        return "Patient-centered clinical workspace";
    if (pathname.startsWith("/appointments"))
        return "Schedule and visit tracking";
    if (pathname.startsWith("/reports"))
        return "Radiology, lab, and discharge documentation";
    if (pathname.startsWith("/notes"))
        return "Clinical note management";
    if (pathname.startsWith("/pacs"))
        return "Radiology studies and imaging access";
    return "Medical operations platform";
}
export default function AppLayout() {
    const location = useLocation();
    const user = getUser();
    const title = getPageTitle(location.pathname);
    const subtitle = getPageSubtitle(location.pathname);
    return (_jsxs("div", { style: {
            display: "flex",
            minHeight: "100vh",
            background: "#020617",
        }, children: [_jsx(AppSidebar, {}), _jsxs("div", { style: { flex: 1, display: "flex", flexDirection: "column" }, children: [_jsx("header", { style: {
                            position: "sticky",
                            top: 0,
                            zIndex: 10,
                            background: "rgba(2, 6, 23, 0.92)",
                            backdropFilter: "blur(8px)",
                            borderBottom: "1px solid #1e293b",
                            padding: "18px 28px",
                        }, children: _jsxs("div", { style: {
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                gap: 16,
                            }, children: [_jsxs("div", { children: [_jsx("div", { style: { color: "white", fontSize: 24, fontWeight: 800 }, children: title }), _jsx("div", { style: { color: "#94a3b8", fontSize: 14, marginTop: 4 }, children: subtitle })] }), _jsxs("div", { style: {
                                        background: "#0f172a",
                                        border: "1px solid #1e293b",
                                        borderRadius: 14,
                                        padding: "10px 14px",
                                        minWidth: 180,
                                    }, children: [_jsx("div", { style: { color: "#94a3b8", fontSize: 12 }, children: "Current user" }), _jsx("div", { style: { color: "white", fontWeight: 700, marginTop: 2 }, children: user?.name ?? "Guest" }), _jsx("div", { style: { color: "#38bdf8", fontSize: 13, marginTop: 2 }, children: user?.role ?? "No role" })] })] }) }), _jsx("main", { style: { padding: 28, color: "white", flex: 1 }, children: _jsx("div", { style: {
                                maxWidth: 1400,
                            }, children: _jsx(Outlet, {}) }) })] })] }));
}
