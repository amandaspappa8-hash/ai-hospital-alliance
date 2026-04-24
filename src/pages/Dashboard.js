import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
const statusColors = {
    "Active": { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
    "Under Observation": { bg: "#1c1917", color: "#fb923c", glow: "0 0 8px #fb923c44" },
    "Critical": { bg: "#450a0a", color: "#f87171", glow: "0 0 8px #f8717144" },
    "Scheduled": { bg: "#0c1a2e", color: "#60a5fa", glow: "0 0 8px #60a5fa44" },
    "Waiting": { bg: "#1c1108", color: "#fbbf24", glow: "0 0 8px #fbbf2444" },
    "Available": { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
    "On Call": { bg: "#1c1108", color: "#fbbf24", glow: "0 0 8px #fbbf2444" },
    "In Surgery": { bg: "#450a0a", color: "#f87171", glow: "0 0 8px #f8717144" },
    "Offline": { bg: "#1e1e1e", color: "#64748b", glow: "none" },
    "Completed": { bg: "#052e16", color: "#4ade80", glow: "0 0 8px #4ade8044" },
};
function Badge({ status }) {
    const s = statusColors[status] ?? { bg: "#1e293b", color: "#94a3b8", glow: "none" };
    return (_jsx("span", { style: {
            background: s.bg, color: s.color, padding: "3px 10px", borderRadius: 20,
            fontSize: 11, fontWeight: 700, whiteSpace: "nowrap",
            boxShadow: s.glow, border: `1px solid ${s.color}33`,
        }, children: status }));
}
function StatCard({ label, value, icon, gradient, sub, to }) {
    return (_jsx(Link, { to: to, style: { textDecoration: "none" }, children: _jsxs("div", { style: {
                background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
                border: "1px solid rgba(99,179,237,0.15)",
                borderRadius: 20, padding: "22px 24px",
                display: "flex", alignItems: "center", gap: 18, cursor: "pointer",
                boxShadow: "0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05)",
                transition: "all 0.3s",
                position: "relative", overflow: "hidden",
            }, onMouseEnter: e => { e.currentTarget.style.borderColor = "rgba(99,179,237,0.4)"; e.currentTarget.style.transform = "translateY(-2px)"; }, onMouseLeave: e => { e.currentTarget.style.borderColor = "rgba(99,179,237,0.15)"; e.currentTarget.style.transform = "translateY(0)"; }, children: [_jsx("div", { style: {
                        position: "absolute", top: 0, right: 0, width: 120, height: 120,
                        background: gradient, borderRadius: "0 20px 0 120px", opacity: 0.15,
                    } }), _jsx("div", { style: {
                        width: 56, height: 56, borderRadius: 16,
                        background: gradient, display: "flex", alignItems: "center",
                        justifyContent: "center", flexShrink: 0,
                        boxShadow: `0 0 20px ${gradient.includes("59,130") ? "rgba(59,130,246,0.4)" : "rgba(168,85,247,0.4)"}`,
                    }, children: icon }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 32, fontWeight: 900, color: "white", lineHeight: 1, letterSpacing: -1 }, children: value }), _jsx("div", { style: { fontSize: 13, color: "#94a3b8", marginTop: 4, fontWeight: 500 }, children: label }), sub && _jsx("div", { style: { fontSize: 11, color: "#4ade80", marginTop: 3, fontWeight: 600 }, children: sub })] })] }) }));
}
function SectionCard({ title, children, to, accent = "#3b82f6" }) {
    return (_jsxs("div", { style: {
            background: "linear-gradient(135deg, #0f172a 0%, #1a2540 100%)",
            border: `1px solid ${accent}22`,
            borderRadius: 20, padding: 22,
            boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
        }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 18 }, children: [_jsxs("div", { style: {
                            fontWeight: 800, fontSize: 15, color: "white",
                            display: "flex", alignItems: "center", gap: 8,
                        }, children: [_jsx("div", { style: { width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` } }), title] }), to && (_jsx(Link, { to: to, style: {
                            color: accent, fontSize: 12, textDecoration: "none", fontWeight: 600,
                            padding: "4px 12px", border: `1px solid ${accent}44`, borderRadius: 20,
                        }, children: "View all \u2192" }))] }), children] }));
}
// ── SVG Icons ────────────────────────────────────────────────────────────────
const Icons = {
    patients: (_jsxs("svg", { width: "26", height: "26", viewBox: "0 0 24 24", fill: "none", stroke: "white", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" }), _jsx("circle", { cx: "9", cy: "7", r: "4" }), _jsx("path", { d: "M23 21v-2a4 4 0 0 0-3-3.87" }), _jsx("path", { d: "M16 3.13a4 4 0 0 1 0 7.75" })] })),
    calendar: (_jsxs("svg", { width: "26", height: "26", viewBox: "0 0 24 24", fill: "none", stroke: "white", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("rect", { x: "3", y: "4", width: "18", height: "18", rx: "2", ry: "2" }), _jsx("line", { x1: "16", y1: "2", x2: "16", y2: "6" }), _jsx("line", { x1: "8", y1: "2", x2: "8", y2: "6" }), _jsx("line", { x1: "3", y1: "10", x2: "21", y2: "10" }), _jsx("path", { d: "M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" })] })),
    alert: (_jsxs("svg", { width: "26", height: "26", viewBox: "0 0 24 24", fill: "none", stroke: "white", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" }), _jsx("line", { x1: "12", y1: "9", x2: "12", y2: "13" }), _jsx("line", { x1: "12", y1: "17", x2: "12.01", y2: "17" })] })),
    doctor: (_jsxs("svg", { width: "26", height: "26", viewBox: "0 0 24 24", fill: "none", stroke: "white", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M12 2a5 5 0 1 0 0 10A5 5 0 0 0 12 2z" }), _jsx("path", { d: "M2 20c0-4 4-7 10-7s10 3 10 7" }), _jsx("path", { d: "M17 13v4m-2-2h4" })] })),
    bell: (_jsxs("svg", { width: "26", height: "26", viewBox: "0 0 24 24", fill: "none", stroke: "white", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" }), _jsx("path", { d: "M13.73 21a2 2 0 0 1-3.46 0" }), _jsx("circle", { cx: "19", cy: "5", r: "3", fill: "#f87171", stroke: "none" })] })),
    radiology: (_jsxs("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("rect", { x: "3", y: "3", width: "18", height: "18", rx: "2" }), _jsx("circle", { cx: "12", cy: "12", r: "3" }), _jsx("line", { x1: "12", y1: "3", x2: "12", y2: "9" }), _jsx("line", { x1: "12", y1: "15", x2: "12", y2: "21" }), _jsx("line", { x1: "3", y1: "12", x2: "9", y2: "12" }), _jsx("line", { x1: "15", y1: "12", x2: "21", y2: "12" })] })),
    lab: (_jsx("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: _jsx("path", { d: "M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v11l-4 5h14l-4-5V3" }) })),
    pharmacy: (_jsx("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: _jsx("path", { d: "M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" }) })),
    pacs: (_jsxs("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("rect", { x: "2", y: "3", width: "20", height: "14", rx: "2" }), _jsx("line", { x1: "8", y1: "21", x2: "16", y2: "21" }), _jsx("line", { x1: "12", y1: "17", x2: "12", y2: "21" }), _jsx("circle", { cx: "12", cy: "10", r: "3" }), _jsx("line", { x1: "7", y1: "7", x2: "7", y2: "7" })] })),
    ai: (_jsxs("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" }), _jsx("circle", { cx: "9", cy: "13", r: "1", fill: "currentColor" }), _jsx("circle", { cx: "15", cy: "13", r: "1", fill: "currentColor" })] })),
    reports: (_jsxs("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" }), _jsx("polyline", { points: "14 2 14 8 20 8" }), _jsx("line", { x1: "16", y1: "13", x2: "8", y2: "13" }), _jsx("line", { x1: "16", y1: "17", x2: "8", y2: "17" }), _jsx("polyline", { points: "10 9 9 9 8 9" })] })),
    nursing: (_jsx("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: _jsx("path", { d: "M22 12h-4l-3 9L9 3l-3 9H2" }) })),
    specialties: (_jsxs("svg", { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", strokeLinecap: "round", strokeLinejoin: "round", children: [_jsx("path", { d: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" }), _jsx("polyline", { points: "9 22 9 12 15 12 15 22" })] })),
};
const quickLinks = [
    { label: "Radiology", icon: Icons.radiology, to: "/radiology", color: "#06b6d4" },
    { label: "Labs", icon: Icons.lab, to: "/labs", color: "#a78bfa" },
    { label: "Pharmacy", icon: Icons.pharmacy, to: "/pharmacy", color: "#f43f5e" },
    { label: "PACS", icon: Icons.pacs, to: "/pacs", color: "#0ea5e9" },
    { label: "AI Engine", icon: Icons.ai, to: "/ai-routing", color: "#10b981" },
    { label: "Reports", icon: Icons.reports, to: "/reports", color: "#f59e0b" },
    { label: "Nursing", icon: Icons.nursing, to: "/nursing", color: "#ec4899" },
    { label: "Specialties", icon: Icons.specialties, to: "/specialties", color: "#8b5cf6" },
];
const deptList = [
    { name: "Cardiology", color: "#f43f5e", to: "/specialties/cardiology",
        icon: _jsx("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: _jsx("path", { d: "M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" }) }) },
    { name: "Neurology", color: "#a78bfa", to: "/specialties/neurology",
        icon: _jsxs("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: [_jsx("circle", { cx: "12", cy: "12", r: "10" }), _jsx("path", { d: "M12 8v4l3 3" })] }) },
    { name: "Emergency", color: "#f97316", to: "/specialties/emergency",
        icon: _jsx("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: _jsx("polygon", { points: "13 2 3 14 12 14 11 22 21 10 12 10 13 2" }) }) },
    { name: "ICU", color: "#06b6d4", to: "/specialties/icu",
        icon: _jsx("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: _jsx("path", { d: "M22 12h-4l-3 9L9 3l-3 9H2" }) }) },
    { name: "Pediatrics", color: "#fbbf24", to: "/specialties/pediatrics",
        icon: _jsxs("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: [_jsx("path", { d: "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" }), _jsx("circle", { cx: "9", cy: "7", r: "4" }), _jsx("path", { d: "M23 21v-2a4 4 0 0 0-3-3.87" })] }) },
    { name: "Radiology", color: "#10b981", to: "/radiology",
        icon: _jsxs("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "1.5", children: [_jsx("rect", { x: "3", y: "3", width: "18", height: "18", rx: "2" }), _jsx("circle", { cx: "12", cy: "12", r: "3" })] }) },
];
export default function Dashboard() {
    const user = getUser();
    const [patients, setPatients] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        Promise.all([
            apiGet("/patients").catch(() => []),
            apiGet("/appointments").catch(() => []),
            apiGet("/alerts").catch(() => []),
            apiGet("/doctors/summary").catch(() => []),
        ]).then(([p, a, al, d]) => {
            setPatients(Array.isArray(p) ? p : []);
            setAppointments(Array.isArray(a) ? a : []);
            setAlerts(Array.isArray(al) ? al : []);
            setDoctors(Array.isArray(d) ? d : []);
        }).finally(() => setLoading(false));
    }, []);
    const critical = patients.filter(p => p.status === "Critical").length;
    const available = doctors.filter(d => d.status === "Available").length;
    return (_jsxs("div", { style: {
            background: "linear-gradient(135deg, #020817 0%, #0f1629 50%, #0a1628 100%)",
            padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
        }, children: [_jsx("div", { style: {
                    position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
                    backgroundImage: "linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px)",
                    backgroundSize: "60px 60px",
                } }), _jsxs("div", { style: { position: "relative", zIndex: 1, maxWidth: 1400, margin: "0 auto" }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 32 }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 COMMAND CENTER" }), _jsxs("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, letterSpacing: -0.5,
                                            background: "linear-gradient(135deg, #fff 0%, #94a3b8 100%)",
                                            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }, children: ["Welcome, ", user?.name ?? "Doctor", " \uD83D\uDC4B"] }), _jsxs("p", { style: { margin: "6px 0 0", color: "#475569", fontSize: 13, fontWeight: 500 }, children: [user?.role, " \u00B7 ", new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" })] })] }), _jsxs("div", { style: { display: "flex", gap: 10 }, children: [_jsx(Link, { to: "/patients", style: {
                                            background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
                                            color: "white", padding: "11px 20px", borderRadius: 12, textDecoration: "none",
                                            fontSize: 13, fontWeight: 700, boxShadow: "0 0 20px rgba(37,99,235,0.4)",
                                            border: "1px solid rgba(99,179,237,0.3)",
                                        }, children: "+ New Patient" }), _jsx(Link, { to: "/appointments", style: {
                                            background: "rgba(255,255,255,0.05)", color: "white", padding: "11px 20px",
                                            borderRadius: 12, textDecoration: "none", fontSize: 13, fontWeight: 700,
                                            border: "1px solid rgba(255,255,255,0.1)", backdropFilter: "blur(10px)",
                                        }, children: "\uD83D\uDCC5 Schedule" })] })] }), loading ? (_jsx("div", { style: { color: "#3b82f6", marginBottom: 28, fontSize: 14 }, children: "\u27F3 Loading systems..." })) : (_jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: 16, marginBottom: 28 }, children: [_jsx(StatCard, { label: "Total Patients", value: patients.length, icon: Icons.patients, gradient: "linear-gradient(135deg,#2563eb,#7c3aed)", sub: "\u2191 47% from last month", to: "/patients" }), _jsx(StatCard, { label: "Appointments Today", value: appointments.length, icon: Icons.calendar, gradient: "linear-gradient(135deg,#7c3aed,#a855f7)", sub: "\u2191 12% from last month", to: "/appointments" }), _jsx(StatCard, { label: "Critical Patients", value: critical, icon: Icons.alert, gradient: "linear-gradient(135deg,#dc2626,#b91c1c)", sub: "Requires attention", to: "/patients" }), _jsx(StatCard, { label: "Available Doctors", value: available, icon: Icons.doctor, gradient: "linear-gradient(135deg,#059669,#047857)", sub: "On duty now", to: "/doctors" }), _jsx(StatCard, { label: "Active Alerts", value: alerts.length, icon: Icons.bell, gradient: "linear-gradient(135deg,#d97706,#b45309)", sub: "Requires review", to: "/alerts" })] })), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 300px", gap: 20, marginBottom: 20 }, children: [_jsx(SectionCard, { title: "Recent Patients", to: "/patients", accent: "#3b82f6", children: patients.length === 0 ? _jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No patients." }) : (_jsxs("table", { style: { width: "100%", borderCollapse: "collapse", fontSize: 13 }, children: [_jsx("thead", { children: _jsx("tr", { children: ["Patient", "Dept", "Status", ""].map(h => (_jsx("th", { style: { textAlign: "left", paddingBottom: 12, color: "#475569", fontWeight: 600, fontSize: 11, textTransform: "uppercase", letterSpacing: 1 }, children: h }, h))) }) }), _jsx("tbody", { children: patients.slice(0, 6).map((p, i) => (_jsxs("tr", { style: { borderTop: "1px solid rgba(255,255,255,0.04)" }, children: [_jsx("td", { style: { padding: "11px 0" }, children: _jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10 }, children: [_jsx("div", { style: {
                                                                        width: 32, height: 32, borderRadius: 10, flexShrink: 0,
                                                                        background: "linear-gradient(135deg,#1e3a5f,#2563eb22)",
                                                                        border: "1px solid rgba(59,130,246,0.3)",
                                                                        display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14,
                                                                    }, children: "\uD83D\uDC64" }), _jsxs("div", { children: [_jsx("div", { style: { fontWeight: 700, color: "white" }, children: p.name }), _jsx("div", { style: { color: "#475569", fontSize: 11 }, children: p.id })] })] }) }), _jsx("td", { style: { padding: "11px 0", color: "#64748b" }, children: p.department ?? "—" }), _jsx("td", { style: { padding: "11px 0" }, children: _jsx(Badge, { status: p.status }) }), _jsx("td", { style: { padding: "11px 0" }, children: _jsx(Link, { to: `/patients/${p.id}`, style: {
                                                                color: "#3b82f6", fontSize: 12, textDecoration: "none", fontWeight: 600,
                                                                padding: "3px 10px", border: "1px solid rgba(59,130,246,0.3)", borderRadius: 8,
                                                            }, children: "View" }) })] }, p.id))) })] })) }), _jsx(SectionCard, { title: "Today's Appointments", to: "/appointments", accent: "#7c3aed", children: appointments.length === 0 ? _jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No appointments." }) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: appointments.slice(0, 5).map((a) => (_jsxs("div", { style: {
                                            display: "flex", alignItems: "center", gap: 12, padding: "12px 14px",
                                            borderRadius: 12, background: "rgba(124,58,237,0.06)",
                                            border: "1px solid rgba(124,58,237,0.15)",
                                        }, children: [_jsx("div", { style: {
                                                    width: 40, height: 40, borderRadius: 12, flexShrink: 0,
                                                    background: "linear-gradient(135deg,#4c1d95,#7c3aed44)",
                                                    border: "1px solid rgba(124,58,237,0.4)",
                                                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
                                                }, children: "\uD83D\uDC64" }), _jsxs("div", { style: { flex: 1, minWidth: 0 }, children: [_jsx("div", { style: { fontWeight: 700, color: "white", fontSize: 13 }, children: a.patientName }), _jsxs("div", { style: { color: "#64748b", fontSize: 11, marginTop: 2 }, children: [a.doctor, " \u00B7 ", a.time] })] }), _jsx(Badge, { status: a.status })] }, a.id))) })) }), _jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 16 }, children: [_jsx(SectionCard, { title: "Active Alerts", accent: "#ef4444", children: alerts.length === 0 ? (_jsx("div", { style: {
                                                padding: "16px", borderRadius: 12, textAlign: "center",
                                                background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)",
                                                color: "#4ade80", fontSize: 13, fontWeight: 600,
                                            }, children: "\u2713 All systems normal" })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: alerts.slice(0, 3).map((al, i) => (_jsxs("div", { style: {
                                                    padding: "10px 12px", borderRadius: 10,
                                                    background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.2)",
                                                }, children: [_jsx("div", { style: { color: "#fca5a5", fontSize: 11, fontWeight: 700 }, children: al.patient_id ?? "SYSTEM" }), _jsx("div", { style: { color: "#94a3b8", fontSize: 12, marginTop: 2 }, children: al.message })] }, i))) })) }), _jsx(SectionCard, { title: "Quick Access", accent: "#06b6d4", children: _jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }, children: quickLinks.map((item) => (_jsx(Link, { to: item.to, style: { textDecoration: "none" }, children: _jsxs("div", { style: {
                                                        padding: "10px 12px", borderRadius: 10,
                                                        background: `${item.color}08`,
                                                        border: `1px solid ${item.color}22`,
                                                        display: "flex", alignItems: "center", gap: 8,
                                                        color: item.color, fontSize: 12, fontWeight: 600,
                                                        cursor: "pointer", transition: "all 0.2s",
                                                    }, onMouseEnter: e => { e.currentTarget.style.background = `${item.color}18`; e.currentTarget.style.borderColor = `${item.color}55`; }, onMouseLeave: e => { e.currentTarget.style.background = `${item.color}08`; e.currentTarget.style.borderColor = `${item.color}22`; }, children: [item.icon, item.label] }) }, item.to))) }) })] })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }, children: [_jsx(SectionCard, { title: "Doctor Directory", to: "/doctors", accent: "#10b981", children: _jsx("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: doctors.slice(0, 5).map((d) => (_jsxs("div", { style: {
                                            display: "flex", alignItems: "center", gap: 12,
                                            padding: "10px 14px", borderRadius: 12,
                                            background: "rgba(16,185,129,0.04)", border: "1px solid rgba(16,185,129,0.1)",
                                        }, children: [_jsx("div", { style: {
                                                    width: 38, height: 38, borderRadius: 10, flexShrink: 0,
                                                    background: "linear-gradient(135deg,#064e3b,#10b98122)",
                                                    border: "1px solid rgba(16,185,129,0.3)",
                                                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
                                                }, children: "\uD83D\uDC68\u200D\u2695\uFE0F" }), _jsxs("div", { style: { flex: 1 }, children: [_jsx("div", { style: { color: "white", fontWeight: 700, fontSize: 13 }, children: d.name }), _jsxs("div", { style: { color: "#64748b", fontSize: 11, marginTop: 2 }, children: [d.specialty, " \u00B7 \u2B50 ", d.rating] })] }), _jsx(Badge, { status: d.status })] }, d.id))) }) }), _jsx(SectionCard, { title: "Hospital Departments", to: "/specialties", accent: "#f59e0b", children: _jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }, children: deptList.map((s) => (_jsx(Link, { to: s.to, style: { textDecoration: "none" }, children: _jsxs("div", { style: {
                                                padding: "16px 12px", borderRadius: 14, textAlign: "center",
                                                background: `${s.color}08`, border: `1px solid ${s.color}22`,
                                                cursor: "pointer", transition: "all 0.2s",
                                            }, onMouseEnter: e => { e.currentTarget.style.background = `${s.color}18`; e.currentTarget.style.transform = "translateY(-2px)"; }, onMouseLeave: e => { e.currentTarget.style.background = `${s.color}08`; e.currentTarget.style.transform = "translateY(0)"; }, children: [_jsx("div", { style: { color: s.color, marginBottom: 6 }, children: s.icon }), _jsx("div", { style: { color: "white", fontSize: 12, fontWeight: 700 }, children: s.name })] }) }, s.to))) }) })] })] })] }));
}
