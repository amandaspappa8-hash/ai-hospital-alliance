import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState, useCallback } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
const DEPT_COLORS = {
    Cardiology: "#ef4444", Emergency: "#f97316", ICU: "#06b6d4",
    Neurology: "#a855f7", Pediatrics: "#fbbf24", Orthopedics: "#10b981", Radiology: "#3b82f6",
};
const STATUS_COLORS = {
    Active: "#4ade80", "Under Observation": "#fb923c", Critical: "#f87171", Discharged: "#94a3b8"
};
const GENDER_COLORS = { Male: "#3b82f6", Female: "#ec4899" };
// Animated counter hook
function useCounter(target, duration = 1000) {
    const [value, setValue] = useState(0);
    useEffect(() => {
        if (target === 0)
            return;
        const steps = 30;
        const increment = target / steps;
        let current = 0;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                setValue(target);
                clearInterval(timer);
            }
            else
                setValue(Math.round(current));
        }, duration / steps);
        return () => clearInterval(timer);
    }, [target, duration]);
    return value;
}
function KpiCard({ label, value, color, icon, sub }) {
    const numVal = typeof value === "number" ? value : 0;
    const animated = useCounter(numVal);
    return (_jsxs("div", { style: {
            padding: "18px 20px", borderRadius: 18,
            background: `linear-gradient(135deg, ${color}10, ${color}05)`,
            border: `1px solid ${color}30`,
            display: "flex", alignItems: "center", gap: 14,
            transition: "transform 0.2s", cursor: "default",
        }, onMouseEnter: e => (e.currentTarget.style.transform = "translateY(-2px)"), onMouseLeave: e => (e.currentTarget.style.transform = "translateY(0)"), children: [_jsx("div", { style: {
                    width: 46, height: 46, borderRadius: 14,
                    background: `${color}20`, display: "flex",
                    alignItems: "center", justifyContent: "center", fontSize: 22, flexShrink: 0
                }, children: icon }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 24, fontWeight: 900, color, lineHeight: 1 }, children: typeof value === "number" ? animated : value }), _jsx("div", { style: { fontSize: 11, color: "#64748b", marginTop: 3 }, children: label }), sub && _jsx("div", { style: { fontSize: 10, color: color, marginTop: 2, opacity: 0.8 }, children: sub })] })] }));
}
function BarChart({ data, colors, title, accentColor }) {
    const max = Math.max(...Object.values(data), 1);
    const sorted = Object.entries(data).sort((a, b) => b[1] - a[1]);
    return (_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 13, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: accentColor, borderRadius: 2 } }), title] }), sorted.map(([label, value]) => (_jsxs("div", { style: { marginBottom: 14 }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 6 }, children: [_jsx("span", { style: { fontSize: 12, color: "#94a3b8" }, children: label }), _jsx("span", { style: { fontSize: 12, fontWeight: 700, color: colors[label] ?? "#64748b" }, children: value })] }), _jsx("div", { style: { height: 7, borderRadius: 4, background: "rgba(255,255,255,0.06)", overflow: "hidden" }, children: _jsx("div", { style: {
                                height: "100%", width: `${Math.round((value / max) * 100)}%`,
                                background: `linear-gradient(90deg, ${colors[label] ?? "#64748b"}, ${colors[label] ?? "#64748b"}88)`,
                                borderRadius: 4, transition: "width 1.2s cubic-bezier(0.4,0,0.2,1)"
                            } }) })] }, label)))] }));
}
function DonutChart({ data, colors, title, accentColor }) {
    const total = Object.values(data).reduce((s, v) => s + v, 0);
    let cumulative = 0;
    const segments = Object.entries(data).map(([label, value]) => {
        const pct = total > 0 ? (value / total) * 100 : 0;
        const start = cumulative;
        cumulative += pct;
        return { label, value, pct, start };
    });
    const r = 38, cx = 50, cy = 50;
    function arc(start, end) {
        const s = (start / 100) * 2 * Math.PI - Math.PI / 2;
        const e = (end / 100) * 2 * Math.PI - Math.PI / 2;
        const x1 = cx + r * Math.cos(s), y1 = cy + r * Math.sin(s);
        const x2 = cx + r * Math.cos(e), y2 = cy + r * Math.sin(e);
        return `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${end - start > 50 ? 1 : 0} 1 ${x2} ${y2} Z`;
    }
    return (_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 13, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: accentColor, borderRadius: 2 } }), title] }), total === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13, textAlign: "center", padding: "20px 0" }, children: "No data" })) : (_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 20 }, children: [_jsxs("svg", { width: "100", height: "100", viewBox: "0 0 100 100", style: { flexShrink: 0 }, children: [segments.map(seg => (_jsx("path", { d: arc(seg.start, seg.start + seg.pct), fill: colors[seg.label] ?? "#64748b", opacity: 0.9 }, seg.label))), _jsx("circle", { cx: cx, cy: cy, r: 20, fill: "#0f172a" }), _jsx("text", { x: cx, y: cy + 4, textAnchor: "middle", fill: "white", fontSize: "10", fontWeight: "800", children: total })] }), _jsx("div", { style: { flex: 1 }, children: segments.map(seg => (_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 6, fontSize: 11 }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 6 }, children: [_jsx("div", { style: { width: 8, height: 8, borderRadius: 2, background: colors[seg.label] ?? "#64748b", flexShrink: 0 } }), _jsx("span", { style: { color: "#94a3b8" }, children: seg.label })] }), _jsxs("span", { style: { color: "white", fontWeight: 700 }, children: [seg.value, " ", _jsxs("span", { style: { color: "#64748b" }, children: ["(", Math.round(seg.pct), "%)"] })] })] }, seg.label))) })] }))] }));
}
function LineChart({ title, accentColor }) {
    // Simulated weekly trend data
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    const admissions = [12, 18, 15, 22, 19, 14, 17];
    const discharges = [8, 12, 10, 16, 14, 10, 13];
    const w = 260, h = 100, padL = 30, padB = 20, padT = 10;
    const maxVal = Math.max(...admissions, ...discharges);
    const toX = (i) => padL + (i / (days.length - 1)) * (w - padL - 10);
    const toY = (v) => padT + ((maxVal - v) / maxVal) * (h - padB - padT);
    const line = (data) => data.map((v, i) => `${i === 0 ? "M" : "L"} ${toX(i)} ${toY(v)}`).join(" ");
    return (_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 13, color: "white", marginBottom: 4, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: accentColor, borderRadius: 2 } }), title] }), _jsx("div", { style: { fontSize: 11, color: "#64748b", marginBottom: 16 }, children: "Weekly patient flow" }), _jsxs("svg", { width: "100%", viewBox: `0 0 ${w} ${h}`, style: { overflow: "visible" }, children: [[0, 0.25, 0.5, 0.75, 1].map(t => (_jsx("line", { x1: padL, x2: w - 10, y1: padT + t * (h - padB - padT), y2: padT + t * (h - padB - padT), stroke: "rgba(255,255,255,0.05)", strokeWidth: "1" }, t))), _jsx("path", { d: line(admissions), fill: "none", stroke: "#3b82f6", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }), _jsx("path", { d: line(discharges), fill: "none", stroke: "#10b981", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round", strokeDasharray: "4 2" }), admissions.map((v, i) => _jsx("circle", { cx: toX(i), cy: toY(v), r: "3", fill: "#3b82f6" }, i)), discharges.map((v, i) => _jsx("circle", { cx: toX(i), cy: toY(v), r: "3", fill: "#10b981" }, i)), days.map((d, i) => (_jsx("text", { x: toX(i), y: h - 2, textAnchor: "middle", fill: "#475569", fontSize: "8", children: d }, d)))] }), _jsx("div", { style: { display: "flex", gap: 16, marginTop: 8 }, children: [{ color: "#3b82f6", label: "Admissions" }, { color: "#10b981", label: "Discharges" }].map(({ color, label }) => (_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#94a3b8" }, children: [_jsx("div", { style: { width: 20, height: 2, background: color, borderRadius: 1 } }), label] }, label))) })] }));
}
function AlertsPanel({ patients }) {
    const critical = patients.filter(p => p.status === "Critical");
    const observation = patients.filter(p => p.status === "Under Observation");
    const alerts = [
        ...critical.map(p => ({ type: "critical", msg: `${p.name} — Critical in ${p.department}`, color: "#ef4444" })),
        ...observation.slice(0, 3).map(p => ({ type: "warning", msg: `${p.name} — Under Observation`, color: "#f97316" })),
    ].slice(0, 6);
    return (_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(239,68,68,0.15)", borderRadius: 20, padding: 22 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 13, color: "white", marginBottom: 16, display: "flex", alignItems: "center", justifyContent: "space-between" }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#ef4444", borderRadius: 2 } }), "Active Alerts"] }), alerts.length > 0 && (_jsxs("div", { style: { fontSize: 10, background: "#ef444420", color: "#ef4444", padding: "2px 8px", borderRadius: 20, fontWeight: 700 }, children: [alerts.length, " ACTIVE"] }))] }), alerts.length === 0 ? (_jsx("div", { style: { color: "#4ade80", fontSize: 13, textAlign: "center", padding: "16px 0" }, children: "\u2705 All systems normal" })) : (alerts.map((alert, i) => (_jsxs("div", { style: {
                    display: "flex", alignItems: "center", gap: 10, padding: "10px 12px",
                    borderRadius: 10, background: `${alert.color}08`, border: `1px solid ${alert.color}20`,
                    marginBottom: 8
                }, children: [_jsx("div", { style: { width: 8, height: 8, borderRadius: "50%", background: alert.color, flexShrink: 0, boxShadow: `0 0 6px ${alert.color}` } }), _jsx("span", { style: { fontSize: 12, color: "#cbd5e1", flex: 1 }, children: alert.msg }), _jsx("span", { style: { fontSize: 10, color: alert.color, fontWeight: 700 }, children: alert.type === "critical" ? "CRITICAL" : "WATCH" })] }, i))))] }));
}
function TopDoctors({ doctors }) {
    const top = [...doctors].sort((a, b) => b.rating - a.rating).slice(0, 5);
    return (_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#131f35)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 22 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 13, color: "white", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#f59e0b", borderRadius: 2 } }), "Top Performing Doctors"] }), top.map((d, i) => (_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 12, marginBottom: 12, padding: "8px 10px", borderRadius: 12, background: i === 0 ? "rgba(245,158,11,0.06)" : "transparent" }, children: [_jsxs("div", { style: {
                            width: 28, height: 28, borderRadius: 8, flexShrink: 0,
                            background: i === 0 ? "linear-gradient(135deg,#f59e0b,#d97706)" : "rgba(255,255,255,0.06)",
                            display: "flex", alignItems: "center", justifyContent: "center",
                            fontSize: 12, fontWeight: 800, color: i === 0 ? "white" : "#64748b"
                        }, children: ["#", i + 1] }), _jsxs("div", { style: { flex: 1, minWidth: 0 }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 700, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }, children: d.name }), _jsx("div", { style: { fontSize: 10, color: "#64748b" }, children: d.specialty })] }), _jsxs("div", { style: { textAlign: "right", flexShrink: 0 }, children: [_jsxs("div", { style: { fontSize: 13, fontWeight: 800, color: "#f59e0b" }, children: ["\u2B50 ", d.rating] }), _jsxs("div", { style: { fontSize: 10, color: "#64748b" }, children: [d.patients_count, " pts"] })] })] }, d.id)))] }));
}
export default function AdminOverviewPage() {
    const user = getUser();
    const [patients, setPatients] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [lastRefresh, setLastRefresh] = useState(new Date());
    const [timeFilter, setTimeFilter] = useState("today");
    const fetchData = useCallback(() => {
        setLoading(true);
        Promise.all([
            apiGet("/patients").catch(() => []),
            apiGet("/doctors/summary").catch(() => []),
            apiGet("/appointments").catch(() => []),
        ]).then(([p, d, a]) => {
            setPatients(Array.isArray(p) ? p : []);
            setDoctors(Array.isArray(d) ? d : []);
            setAppointments(Array.isArray(a) ? a : []);
            setLastRefresh(new Date());
        }).finally(() => setLoading(false));
    }, []);
    useEffect(() => { fetchData(); }, [fetchData]);
    // Analytics
    const deptCount = patients.reduce((a, p) => { a[p.department] = (a[p.department] || 0) + 1; return a; }, {});
    const statusCount = patients.reduce((a, p) => { a[p.status] = (a[p.status] || 0) + 1; return a; }, {});
    const genderCount = patients.reduce((a, p) => { a[p.gender] = (a[p.gender] || 0) + 1; return a; }, {});
    const availDoctors = doctors.filter(d => d.status === "Available").length;
    const avgRating = doctors.length > 0 ? (doctors.reduce((s, d) => s + d.rating, 0) / doctors.length).toFixed(1) : "—";
    const criticalRate = patients.length > 0 ? Math.round(((statusCount["Critical"] ?? 0) / patients.length) * 100) : 0;
    const occupancyRate = Math.min(Math.round((patients.length / Math.max(doctors.length * 10, 1)) * 100), 100);
    const appointmentStatus = appointments.reduce((a, ap) => {
        a[ap.status] = (a[ap.status] || 0) + 1;
        return a;
    }, {});
    return (_jsxs("div", { style: { padding: "24px 28px", fontFamily: "Inter,Arial,sans-serif", color: "white", minHeight: "100vh", maxWidth: 1400 }, children: [_jsxs("div", { style: { marginBottom: 24, display: "flex", alignItems: "flex-start", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontSize: 11, color: "#6366f1", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 ANALYTICS" }), _jsx("h1", { style: { margin: 0, fontSize: 26, fontWeight: 900, color: "white" }, children: "\uD83D\uDCCA Hospital Analytics Dashboard" }), _jsxs("p", { style: { color: "#475569", fontSize: 12, marginTop: 4 }, children: [new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" }), " · ", user?.name, " · ", _jsx("span", { style: { color: "#4ade80" }, children: "\u25CF" }), " Live"] })] }), _jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10 }, children: [_jsx("div", { style: { display: "flex", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 10, overflow: "hidden" }, children: ["today", "week", "month"].map(t => (_jsx("button", { onClick: () => setTimeFilter(t), style: {
                                        padding: "6px 14px", fontSize: 11, fontWeight: 700, border: "none", cursor: "pointer",
                                        background: timeFilter === t ? "#6366f1" : "transparent",
                                        color: timeFilter === t ? "white" : "#64748b",
                                        textTransform: "capitalize", transition: "all 0.2s"
                                    }, children: t }, t))) }), _jsx("button", { onClick: fetchData, style: {
                                    padding: "6px 16px", fontSize: 11, fontWeight: 700,
                                    background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)",
                                    borderRadius: 10, color: "#818cf8", cursor: "pointer"
                                }, children: "\u21BB Refresh" })] })] }), _jsxs("div", { style: { fontSize: 10, color: "#334155", marginBottom: 20 }, children: ["Last updated: ", lastRefresh.toLocaleTimeString()] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12, marginBottom: 20 }, children: [_jsx(KpiCard, { label: "Total Patients", value: patients.length, color: "#3b82f6", icon: "\uD83E\uDDD1\u200D\u2695\uFE0F", sub: `${statusCount["Active"] ?? 0} active` }), _jsx(KpiCard, { label: "Available Doctors", value: availDoctors, color: "#10b981", icon: "\uD83D\uDC68\u200D\u2695\uFE0F", sub: `of ${doctors.length} total` }), _jsx(KpiCard, { label: "Appointments", value: appointments.length, color: "#a855f7", icon: "\uD83D\uDCC5", sub: `${appointmentStatus["Scheduled"] ?? 0} scheduled` }), _jsx(KpiCard, { label: "Critical Cases", value: statusCount["Critical"] ?? 0, color: "#ef4444", icon: "\u26A0\uFE0F", sub: `${criticalRate}% rate` }), _jsx(KpiCard, { label: "Avg Doctor Rating", value: avgRating, color: "#f59e0b", icon: "\u2B50", sub: "out of 5.0" }), _jsx(KpiCard, { label: "Bed Occupancy", value: `${occupancyRate}%`, color: "#06b6d4", icon: "\uD83C\uDFE5", sub: "estimated" })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginBottom: 16 }, children: [_jsx(BarChart, { data: deptCount, colors: DEPT_COLORS, title: "Patients by Department", accentColor: "#6366f1" }), _jsx(DonutChart, { data: statusCount, colors: STATUS_COLORS, title: "Patient Status Distribution", accentColor: "#10b981" }), _jsx(DonutChart, { data: genderCount, colors: GENDER_COLORS, title: "Gender Distribution", accentColor: "#ec4899" })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 16, marginBottom: 16 }, children: [_jsx(LineChart, { title: "Patient Flow Trend", accentColor: "#3b82f6" }), _jsx(TopDoctors, { doctors: doctors }), _jsx(AlertsPanel, { patients: patients })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }, children: [
                    {
                        title: "Busiest Department",
                        value: Object.entries(deptCount).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "—",
                        sub: `${Object.entries(deptCount).sort((a, b) => b[1] - a[1])[0]?.[1] ?? 0} patients`,
                        icon: "🏥", color: "#6366f1"
                    },
                    {
                        title: "Under Observation",
                        value: statusCount["Under Observation"] ?? 0,
                        sub: "needs monitoring",
                        icon: "👁️", color: "#f97316"
                    },
                    {
                        title: "Discharged Today",
                        value: statusCount["Discharged"] ?? 0,
                        sub: "successfully",
                        icon: "✅", color: "#10b981"
                    },
                    {
                        title: "Critical Rate",
                        value: `${criticalRate}%`,
                        sub: criticalRate > 10 ? "⚠️ Above average" : "✅ Normal range",
                        icon: "📊", color: criticalRate > 10 ? "#ef4444" : "#4ade80"
                    },
                ].map(({ title, value, sub, icon, color }) => (_jsxs("div", { style: {
                        padding: "18px 20px", borderRadius: 18,
                        background: "linear-gradient(135deg,#0f172a,#131f35)",
                        border: `1px solid ${color}20`,
                        transition: "transform 0.2s", cursor: "default"
                    }, onMouseEnter: e => (e.currentTarget.style.transform = "translateY(-2px)"), onMouseLeave: e => (e.currentTarget.style.transform = "translateY(0)"), children: [_jsx("div", { style: { fontSize: 26, marginBottom: 10 }, children: icon }), _jsx("div", { style: { fontSize: 20, fontWeight: 900, color }, children: value }), _jsx("div", { style: { fontSize: 12, color: "white", marginTop: 4, fontWeight: 600 }, children: title }), _jsx("div", { style: { fontSize: 11, color: "#64748b", marginTop: 3 }, children: sub })] }, title))) }), loading && (_jsx("div", { style: {
                    position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)",
                    display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50
                }, children: _jsx("div", { style: { fontSize: 14, color: "#818cf8", fontWeight: 700 }, children: "\u23F3 Loading analytics..." }) }))] }));
}
