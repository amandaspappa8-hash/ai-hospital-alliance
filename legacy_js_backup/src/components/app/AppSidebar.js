import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { NavLink, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { FlaskConical, LayoutDashboard, Brain, ClipboardList, Users, UserSquare2, CalendarDays, FileText, NotebookPen, ScanSearch, LogOut, Pill, ShieldPlus, Stethoscope, Building2, HeartPulse, BrainCircuit, Ambulance, ActivitySquare, ScanLine, Baby, BarChart3, } from "lucide-react";
import { getUser } from "@/lib/auth-storage";
import { getSpecialtiesSummary } from "@/lib/specialties";
const items = [
    {
        title: "Dashboard",
        to: "/dashboard",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(LayoutDashboard, { size: 18 }),
    },
    {
        title: "Admin Overview",
        to: "/admin-overview",
        roles: ["Admin"],
        icon: _jsx(BarChart3, { size: 18 }),
    },
    {
        title: "AI Routing",
        to: "/ai-routing",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Brain, { size: 18 }),
    },
    {
        title: "Clinical Decision",
        to: "/clinical-decision",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ShieldPlus, { size: 18 }),
    },
    {
        title: "Orders",
        to: "/orders",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ClipboardList, { size: 18 }),
    },
    {
        title: "Doctors",
        to: "/doctors",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Stethoscope, { size: 18 }),
    },
    {
        title: "Specialties",
        to: "/specialties",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Building2, { size: 18 }),
    },
    {
        title: "Patients",
        to: "/patients",
        roles: ["Admin", "Doctor"],
        icon: _jsx(Users, { size: 18 }),
    },
    {
        title: "Patient Profile",
        to: "/patient-profile",
        roles: ["Admin", "Doctor"],
        icon: _jsx(UserSquare2, { size: 18 }),
    },
    {
        title: "Appointments",
        to: "/appointments",
        roles: ["Admin", "Doctor"],
        icon: _jsx(CalendarDays, { size: 18 }),
    },
    {
        title: "Reports",
        to: "/reports",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(FileText, { size: 18 }),
    },
    {
        title: "Notes",
        to: "/notes",
        roles: ["Admin", "Doctor"],
        icon: _jsx(NotebookPen, { size: 18 }),
    },
    {
        title: "PACS",
        to: "/pacs",
        roles: ["Admin", "Radiology"],
        icon: _jsx(ScanSearch, { size: 18 }),
    },
    {
        title: "Labs",
        to: "/labs",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(FlaskConical, { size: 18 }),
    },
    {
        title: "Nurses",
        to: "/nurses",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Users, { size: 18 }),
    },
    {
        title: "Radiology",
        to: "/radiology",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ScanLine, { size: 18 }),
    },
    {
        title: "Pharmacy",
        to: "/pharmacy",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Pill, { size: 18 }),
    },
    {
        title: "Logout",
        to: "/logout",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(LogOut, { size: 18 }),
    },
];
const specialtyIconMap = {
    Cardiology: _jsx(HeartPulse, { size: 16 }),
    Neurology: _jsx(BrainCircuit, { size: 16 }),
    Emergency: _jsx(Ambulance, { size: 16 }),
    ICU: _jsx(ActivitySquare, { size: 16 }),
    Radiology: _jsx(ScanLine, { size: 16 }),
    Pediatrics: _jsx(Baby, { size: 16 }),
};
export default function AppSidebar() {
    const user = getUser();
    const role = user?.role;
    const location = useLocation();
    const [specialties, setSpecialties] = useState([]);
    useEffect(() => {
        async function loadSpecialties() {
            try {
                const data = await getSpecialtiesSummary();
                setSpecialties(data);
            }
            catch (err) {
                console.error("Failed to load specialties summary", err);
                setSpecialties([]);
            }
        }
        loadSpecialties();
    }, []);
    const visibleItems = role
        ? items.filter((item) => item.roles.includes(role))
        : [];
    const showSpecialtyChildren = location.pathname.startsWith("/specialties");
    return (_jsxs("aside", { style: {
            width: 280,
            padding: 20,
            background: "#0f172a",
            color: "white",
            minHeight: "100vh",
            borderRight: "1px solid #1e293b",
            display: "flex",
            flexDirection: "column",
        }, children: [_jsxs("div", { style: {
                    padding: "8px 4px 18px",
                    borderBottom: "1px solid #1e293b",
                    marginBottom: 18,
                }, children: [_jsx("div", { style: { fontWeight: 800, fontSize: 22, letterSpacing: 0.2 }, children: "AI Hospital Alliance" }), _jsx("div", { style: { fontSize: 13, opacity: 0.7, marginTop: 6 }, children: "Intelligent clinical operations" })] }), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #1f2937",
                    borderRadius: 14,
                    padding: 14,
                    marginBottom: 18,
                }, children: [_jsx("div", { style: { fontSize: 13, opacity: 0.7, marginBottom: 6 }, children: "Signed in as" }), _jsx("div", { style: { fontWeight: 700 }, children: user ? user.name : "Guest" }), _jsx("div", { style: { fontSize: 14, color: "#93c5fd", marginTop: 4 }, children: user ? user.role : "No role" })] }), _jsx("nav", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: visibleItems.map((item) => {
                    const isSpecialtiesRoot = item.to === "/specialties";
                    return (_jsxs("div", { children: [_jsxs(NavLink, { to: item.to, style: ({ isActive }) => ({
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 12,
                                    padding: "12px 14px",
                                    borderRadius: 12,
                                    color: isActive ? "#ffffff" : "#cbd5e1",
                                    background: isActive ? "#0ea5e9" : "transparent",
                                    textDecoration: "none",
                                    fontWeight: isActive ? 700 : 500,
                                    border: isActive ? "1px solid #38bdf8" : "1px solid transparent",
                                }), children: [item.icon, _jsx("span", { children: item.title })] }), isSpecialtiesRoot && showSpecialtyChildren && (_jsx("div", { style: {
                                    marginTop: 8,
                                    marginLeft: 14,
                                    paddingLeft: 12,
                                    borderLeft: "1px solid #1e293b",
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 6,
                                }, children: specialties.map((child) => (_jsxs(NavLink, { to: child.route, style: ({ isActive }) => ({
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "space-between",
                                        gap: 10,
                                        padding: "10px 12px",
                                        borderRadius: 10,
                                        color: isActive ? "#ffffff" : "#94a3b8",
                                        background: isActive ? "#1e293b" : "transparent",
                                        textDecoration: "none",
                                        fontWeight: isActive ? 700 : 500,
                                        fontSize: 14,
                                        border: isActive
                                            ? "1px solid #334155"
                                            : "1px solid transparent",
                                    }), children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10 }, children: [specialtyIconMap[child.title] ?? _jsx(Building2, { size: 16 }), _jsx("span", { children: child.title })] }), _jsx("span", { style: {
                                                minWidth: 28,
                                                height: 22,
                                                borderRadius: 999,
                                                background: "#0f172a",
                                                border: "1px solid #334155",
                                                color: "#cbd5e1",
                                                display: "inline-flex",
                                                alignItems: "center",
                                                justifyContent: "center",
                                                fontSize: 12,
                                                fontWeight: 800,
                                                padding: "0 8px",
                                            }, title: `${child.doctors} doctors`, children: child.doctors })] }, child.route))) }))] }, item.to));
                }) }), _jsx("div", { style: { marginTop: "auto", paddingTop: 20, opacity: 0.55, fontSize: 12 }, children: "Medical Enterprise UI v1" })] }));
}
