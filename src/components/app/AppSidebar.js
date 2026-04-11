import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { NavLink, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { FlaskConical, LayoutDashboard, Brain, ClipboardList, Users, UserSquare2, CalendarDays, FileText, NotebookPen, ScanSearch, LogOut, Pill, ShieldPlus, Stethoscope, Building2, HeartPulse, BrainCircuit, Ambulance, ActivitySquare, ScanLine, Baby, BarChart3, } from "lucide-react";
import { getUser } from "@/lib/auth-storage";
import { getSpecialtiesSummary } from "@/lib/specialties";
import { useAppLanguage } from "@/i18n/useAppLanguage";
const items = [
    {
        titleKey: "nav.dashboard",
        to: "/dashboard",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(LayoutDashboard, { size: 18 }),
    },
    {
        titleKey: "nav.adminOverview",
        to: "/admin-overview",
        roles: ["Admin"],
        icon: _jsx(BarChart3, { size: 18 }),
    },
    {
        titleKey: "nav.aiRouting",
        to: "/ai-routing",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Brain, { size: 18 }),
    },
    {
        titleKey: "nav.clinicalDecision",
        to: "/clinical-decision",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ShieldPlus, { size: 18 }),
    },
    {
        titleKey: "nav.orders",
        to: "/orders",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ClipboardList, { size: 18 }),
    },
    {
        titleKey: "nav.doctors",
        to: "/doctors",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Stethoscope, { size: 18 }),
    },
    {
        titleKey: "nav.specialties",
        to: "/specialties",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Building2, { size: 18 }),
    },
    {
        titleKey: "nav.patients",
        to: "/patients",
        roles: ["Admin", "Doctor"],
        icon: _jsx(Users, { size: 18 }),
    },
    {
        titleKey: "nav.patientProfile",
        to: "/patient-profile",
        roles: ["Admin", "Doctor"],
        icon: _jsx(UserSquare2, { size: 18 }),
    },
    {
        titleKey: "nav.appointments",
        to: "/appointments",
        roles: ["Admin", "Doctor"],
        icon: _jsx(CalendarDays, { size: 18 }),
    },
    {
        titleKey: "nav.reports",
        to: "/reports",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(FileText, { size: 18 }),
    },
    {
        titleKey: "nav.notes",
        to: "/notes",
        roles: ["Admin", "Doctor"],
        icon: _jsx(NotebookPen, { size: 18 }),
    },
    {
        titleKey: "nav.pacs",
        to: "/pacs",
        roles: ["Admin", "Radiology"],
        icon: _jsx(ScanSearch, { size: 18 }),
    },
    {
        titleKey: "nav.labs",
        to: "/labs",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(FlaskConical, { size: 18 }),
    },
    {
        titleKey: "nav.nurses",
        to: "/nurses",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Users, { size: 18 }),
    },
    {
        titleKey: "nav.radiology",
        to: "/radiology",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(ScanLine, { size: 18 }),
    },
    {
        titleKey: "nav.pharmacy",
        to: "/pharmacy",
        roles: ["Admin", "Doctor", "Radiology"],
        icon: _jsx(Pill, { size: 18 }),
    },
    {
        titleKey: "nav.logout",
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
    const { t, language, setLanguage } = useAppLanguage();
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
    const visibleItems = role ? items.filter((item) => item.roles.includes(role)) : [];
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
                }, children: [_jsx("div", { style: { fontWeight: 800, fontSize: 22, letterSpacing: 0.2 }, children: t("app.name") }), _jsx("div", { style: { fontSize: 13, opacity: 0.7, marginTop: 6 }, children: t("app.tagline") })] }), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #1f2937",
                    borderRadius: 14,
                    padding: 14,
                    marginBottom: 18,
                }, children: [_jsx("div", { style: { fontSize: 13, opacity: 0.7, marginBottom: 6 }, children: t("user.signedInAs") }), _jsx("div", { style: { fontWeight: 700 }, children: user ? user.name : t("user.guest") }), _jsx("div", { style: { fontSize: 14, color: "#93c5fd", marginTop: 4 }, children: user ? user.role : t("user.noRole") })] }), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #1f2937",
                    borderRadius: 14,
                    padding: 14,
                    marginBottom: 18,
                }, children: [_jsx("div", { style: { fontSize: 13, opacity: 0.7, marginBottom: 8 }, children: t("label.language") }), _jsxs("select", { value: language, onChange: (e) => setLanguage(e.target.value), style: {
                            width: "100%",
                            background: "#020617",
                            color: "white",
                            border: "1px solid #334155",
                            borderRadius: 10,
                            padding: "10px 12px",
                        }, children: [_jsx("option", { value: "en", children: "English" }), _jsx("option", { value: "ar", children: "\u0627\u0644\u0639\u0631\u0628\u064A\u0629" }), _jsx("option", { value: "fr", children: "Fran\u00E7ais" }), _jsx("option", { value: "it", children: "Italiano" }), _jsx("option", { value: "tzm", children: "Tamazi\u0263t" })] })] }), _jsx("nav", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: visibleItems.map((item) => {
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
                                }), children: [item.icon, _jsx("span", { children: t(item.titleKey) })] }), isSpecialtiesRoot && showSpecialtyChildren && (_jsx("div", { style: {
                                    marginTop: 8,
                                    marginLeft: 12,
                                    paddingLeft: 12,
                                    borderLeft: "1px dashed #334155",
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 8,
                                }, children: specialties.map((specialty) => (_jsxs(NavLink, { to: specialty.route, style: ({ isActive }) => ({
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "space-between",
                                        gap: 10,
                                        padding: "10px 12px",
                                        borderRadius: 10,
                                        color: isActive ? "#ffffff" : "#cbd5e1",
                                        background: isActive ? "#1d4ed8" : "#0b1220",
                                        textDecoration: "none",
                                        fontSize: 14,
                                        border: "1px solid #1e293b",
                                    }), children: [_jsxs("span", { style: { display: "flex", alignItems: "center", gap: 8 }, children: [specialtyIconMap[specialty.title] ?? _jsx(Building2, { size: 16 }), specialty.title] }), _jsx("span", { style: {
                                                minWidth: 28,
                                                textAlign: "center",
                                                padding: "2px 8px",
                                                borderRadius: 999,
                                                background: "#0f172a",
                                                color: "#7dd3fc",
                                                fontSize: 12,
                                                fontWeight: 700,
                                            }, children: specialty.activeCases })] }, specialty.title))) }))] }, item.to));
                }) })] }));
}
