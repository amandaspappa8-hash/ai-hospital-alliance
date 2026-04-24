import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
export default function AdminOverviewPage() {
    const user = getUser();
    const [patients, setPatients] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        Promise.all([
            apiGet("/patients").catch(() => []),
            apiGet("/doctors/summary").catch(() => []),
            apiGet("/appointments").catch(() => []),
        ]).then(([p, d, a]) => {
            setPatients(Array.isArray(p) ? p : []);
            setDoctors(Array.isArray(d) ? d : []);
            setAppointments(Array.isArray(a) ? a : []);
        }).finally(() => setLoading(false));
    }, []);
    // Analytics calculations
    const deptCount = patients.reduce((a, p) => { a[p.department] = (a[p.department] || 0) + 1; return a; }, {});
    const statusCount = patients.reduce((a, p) => { a[p.status] = (a[p.status] || 0) + 1; return a; }, {});
    const genderCount = patients.reduce((a, p) => { a[p.gender] = (a[p.gender] || 0) + 1; return a; }, {});
    const availDoctors = doctors.filter(d => d.status === "Available").length;
    const avgRating = doctors.length > 0 ? (doctors.reduce((s, d) => s + d.rating, 0) / doctors.length).toFixed(1) : "—";
    const topDept = Object.entries(deptCount).sort((a, b) => b[1] - a[1])[0];
    const totalPatients = doctors.reduce((s, d) => s + (d.patients_count || 0), 0);
    const DEPT_COLORS = {
        Cardiology: "#ef4444", Emergency: "#f97316", ICU: "#06b6d4",
        Neurology: "#a855f7", Pediatrics: "#fbbf24", Orthopedics: "#10b981", Radiology: "#3b82f6",
    };
    function Bar({ label, value, max, color }) {
        return (_jsxs("div", { style: { marginBottom: 12 }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 5 }, children: [_jsx("span", { style: { fontSize: 12, color: "#94a3b8" }, children: label }), _jsx("span", { style: { fontSize: 12, fontWeight: 700, color }, children: value })] }), _jsx("div", { style: { height: 8, borderRadius: 4, background: "rgba(255,255,255,0.06)", overflow: "hidden" }, children: _jsx("div", { style: { height: "100%", width: `${Math.round((value / max) * 100)}%`, background: color, borderRadius: 4, transition: "width 1s ease" } }) })] }));
    }
    function DonutChart({ data, colors }) {
        const total = Object.values(data).reduce((s, v) => s + v, 0);
        if (total === 0)
            return _jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No data" });
        let cumulative = 0;
        const segments = Object.entries(data).map(([label, value]) => {
            const pct = (value / total) * 100;
            const start = cumulative;
            cumulative += pct;
            return { label, value, pct, start };
        });
        const r = 40, cx = 50, cy = 50;
        function describeArc(start, end) {
            const s = (start / 100) * 2 * Math.PI - Math.PI / 2;
            const e = (end / 100) * 2 * Math.PI - Math.PI / 2;
            const x1 = cx + r * Math.cos(s), y1 = cy + r * Math.sin(s);
            const x2 = cx + r * Math.cos(e), y2 = cy + r * Math.sin(e);
            const large = end - start > 50 ? 1 : 0;
            return `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`;
        }
        return (_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 16 }, children: [_jsxs("svg", { width: "100", height: "100", viewBox: "0 0 100 100", children: [segments.map(seg => (_jsx("path", { d: describeArc(seg.start, seg.start + seg.pct), fill: colors[seg.label] ?? "#64748b", opacity: 0.85 }, seg.label))), _jsx("circle", { cx: cx, cy: cy, r: 22, fill: "#0f172a" }), _jsx("text", { x: cx, y: cy + 5, textAnchor: "middle", fill: "white", fontSize: "11", fontWeight: "700", children: total })] }), _jsx("div", { style: { flex: 1 }, children: segments.map(seg => (_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 4, fontSize: 11 }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 6 }, children: [_jsx("div", { style: { width: 8, height: 8, borderRadius: 2, background: colors[seg.label] ?? "#64748b", flexShrink: 0 } }), _jsx("span", { style: { color: "#94a3b8" }, children: seg.label })] }), _jsxs("span", { style: { color: "white", fontWeight: 700 }, children: [seg.value, " (", Math.round(seg.pct), "%)"] })] }, seg.label))) })] }));
    }
    const STATUS_COLORS = { Active: "#4ade80", "Under Observation": "#fb923c", Critical: "#f87171", Discharged: "#94a3b8" };
    const GENDER_COLORS = { Male: "#3b82f6", Female: "#ec4899" };
    return (_jsxs("div", { style: { padding: "24px 28px", fontFamily: "Inter,Arial,sans-serif", color: "white", minHeight: "100vh" }, children: [_jsxs("div", { style: { marginBottom: 22 }, children: [_jsx("div", { style: { fontSize: 11, color: "#6366f1", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 ANALYTICS" }), _jsx("h1", { style: { margin: 0, fontSize: 26, fontWeight: 900, color: "white" }, children: "\uD83D\uDCCA Hospital Analytics Dashboard" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 4 }, children: ["Real-time insights \u00B7 ", new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" }), " \u00B7 ", user?.name] })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 12, marginBottom: 20 }, children: [
                    { label: "Total Patients", value: patients.length, color: "#3b82f6", icon: "🧑‍⚕️" },
                    { label: "Active Doctors", value: availDoctors, color: "#10b981", icon: "👨‍⚕️" },
                    { label: "Appointments", value: appointments.length, color: "#a855f7", icon: "📅" },
                    { label: "Critical Cases", value: statusCount["Critical"] ?? 0, color: "#ef4444", icon: "⚠️" },
                    { label: "Avg Doctor Rating", value: avgRating, color: "#f59e0b", icon: "⭐" },
                ].map(({ label, value, color, icon }) => (_jsxs("div", { style: { padding: "16px 18px", borderRadius: 16, background: `${color}08`, border: `1px solid ${color}22`, display: "flex", alignItems: "center", gap: 12 }, children: [_jsx("div", { style: { width: 42, height: 42, borderRadius: 12, background: `${color}18`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }, children: icon }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 22, fontWeight: 900, color }, children: value }), _jsx("div", { style: { fontSize: 11, color: "#64748b", marginTop: 2 }, children: label })] })] }, label))) }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginBottom: 16 }, children: [_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 20, padding: 20 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 14, color: "white", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#6366f1", borderRadius: 2 } }), "Patients by Department"] }), loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading..." }) :
                                Object.entries(deptCount).sort((a, b) => b[1] - a[1]).map(([dept, count]) => (_jsx(Bar, { label: dept, value: count, max: Math.max(...Object.values(deptCount)), color: DEPT_COLORS[dept] ?? "#64748b" }, dept)))] }), _jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 20, padding: 20 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 14, color: "white", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#10b981", borderRadius: 2 } }), "Patient Status"] }), loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading..." }) :
                                _jsx(DonutChart, { data: statusCount, colors: STATUS_COLORS }), _jsxs("div", { style: { marginTop: 16, fontWeight: 800, fontSize: 13, color: "white", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#ec4899", borderRadius: 2 } }), "Gender Distribution"] }), loading ? null : _jsx(DonutChart, { data: genderCount, colors: GENDER_COLORS })] }), _jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 20, padding: 20 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 14, color: "white", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 16, background: "#f59e0b", borderRadius: 2 } }), "Doctor Performance"] }), loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading..." }) :
                                doctors.slice(0, 6).sort((a, b) => b.rating - a.rating).map(d => (_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }, children: [_jsx("div", { style: { width: 30, height: 30, borderRadius: 8, background: "linear-gradient(135deg,#f59e0b,#d97706)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, flexShrink: 0 }, children: "\uD83D\uDC68\u200D\u2695\uFE0F" }), _jsxs("div", { style: { flex: 1, minWidth: 0 }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 700, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }, children: d.name.replace("Dr. ", "") }), _jsx("div", { style: { fontSize: 10, color: "#64748b" }, children: d.specialty })] }), _jsxs("div", { style: { textAlign: "right", flexShrink: 0 }, children: [_jsxs("div", { style: { fontSize: 13, fontWeight: 700, color: "#f59e0b" }, children: ["\u2B50 ", d.rating] }), _jsxs("div", { style: { fontSize: 10, color: "#64748b" }, children: [d.patients_count, "pts"] })] })] }, d.id)))] })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12 }, children: [
                    { title: "Busiest Department", value: topDept ? `${topDept[0]} (${topDept[1]})` : "—", icon: "🏥", color: "#6366f1" },
                    { title: "Total Patient-Doctor", value: totalPatients, icon: "🤝", color: "#10b981" },
                    { title: "Appointment Rate", value: `${appointments.length} today`, icon: "📅", color: "#a855f7" },
                    { title: "Critical Rate", value: `${patients.length > 0 ? Math.round(((statusCount["Critical"] ?? 0) / patients.length) * 100) : 0}%`, icon: "⚠️", color: "#ef4444" },
                ].map(({ title, value, icon, color }) => (_jsxs("div", { style: { padding: "16px 18px", borderRadius: 16, background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${color}22` }, children: [_jsx("div", { style: { fontSize: 24, marginBottom: 8 }, children: icon }), _jsx("div", { style: { fontSize: 18, fontWeight: 900, color }, children: value }), _jsx("div", { style: { fontSize: 11, color: "#64748b", marginTop: 4 }, children: title })] }, title))) })] }));
}
