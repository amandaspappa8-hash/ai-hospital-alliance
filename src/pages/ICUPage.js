import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "@/lib/api";
const META = {
    Cardiology: { icon: "❤️", color: "#ef4444", desc: "Heart Center — ECG, Chest Pain, Vascular" },
    Neurology: { icon: "🧠", color: "#a855f7", desc: "Brain & Nerve — Stroke, EEG, Neuroimaging" },
    Emergency: { icon: "🚑", color: "#f97316", desc: "Emergency Dept — Triage, Rapid Response" },
    ICU: { icon: "🏥", color: "#06b6d4", desc: "Critical Care — Ventilation, Monitoring" },
    Pediatrics: { icon: "🧒", color: "#fbbf24", desc: "Children Care — Growth, Fever, Outpatient" },
};
export default function ICUPage() {
    const meta = META["ICU"];
    const [doctors, setDoctors] = useState([]);
    useEffect(() => {
        apiGet("/doctors/summary")
            .then(d => setDoctors((Array.isArray(d) ? d : []).filter((doc) => doc.specialty === "ICU")))
            .catch(() => setDoctors([]));
    }, []);
    return (_jsx("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: _jsxs("div", { style: { maxWidth: 1100, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx(Link, { to: "/specialties", style: { color: "#64748b", fontSize: 12, textDecoration: "none" }, children: "\u2190 Specialties" }), _jsx("div", { style: { fontSize: 12, color: meta.color, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", margin: "8px 0 4px" }, children: "\u25C8 AI HOSPITAL ALLIANCE" }), _jsxs("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, color: "white" }, children: [meta.icon, " ICU"] }), _jsx("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: meta.desc })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14, marginBottom: 24 }, children: [
                        { label: "Specialists", value: doctors.length || "—", color: meta.color },
                        { label: "Status", value: "Operational", color: "#10b981" },
                        { label: "AI Support", value: "Enabled", color: "#3b82f6" },
                    ].map(({ label, value, color }) => (_jsxs("div", { style: { padding: "16px 18px", borderRadius: 16, background: `${color}08`, border: `1px solid ${color}22` }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: label }), _jsx("div", { style: { fontSize: 22, fontWeight: 900, color, marginTop: 6 }, children: value })] }, label))) }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }, children: [_jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${meta.color}22`, borderRadius: 20, padding: 22 }, children: [_jsx("div", { style: { fontWeight: 800, fontSize: 14, color: "white", marginBottom: 16 }, children: "\uD83D\uDC68\u200D\u2695\uFE0F ICU Specialists" }), doctors.length === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No ICU specialists found." })) : doctors.map(d => (_jsx(Link, { to: `/doctors/${d.id}`, style: { textDecoration: "none" }, children: _jsxs("div", { style: { display: "flex", alignItems: "center", gap: 12, padding: "10px 12px", borderRadius: 12, background: `${meta.color}06`, border: `1px solid ${meta.color}15`, marginBottom: 8, transition: "all 0.2s" }, children: [_jsx("div", { style: { width: 36, height: 36, borderRadius: 10, background: `${meta.color}22`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }, children: "\uD83D\uDC68\u200D\u2695\uFE0F" }), _jsxs("div", { style: { flex: 1 }, children: [_jsx("div", { style: { fontWeight: 700, color: "white", fontSize: 13 }, children: d.name }), _jsxs("div", { style: { color: "#64748b", fontSize: 11 }, children: ["\u2B50 ", d.rating, " \u00B7 ", d.schedule] })] }), _jsx("span", { style: { padding: "2px 8px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: d.status === "Available" ? "rgba(16,185,129,0.15)" : "rgba(251,191,36,0.15)", color: d.status === "Available" ? "#4ade80" : "#fbbf24" }, children: d.status })] }) }, d.id)))] }), _jsx("div", { style: { display: "flex", flexDirection: "column", gap: 14 }, children: _jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${meta.color}22`, borderRadius: 20, padding: 22 }, children: [_jsx("div", { style: { fontWeight: 800, fontSize: 14, color: "white", marginBottom: 14 }, children: "\u26A1 Quick Actions" }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }, children: [
                                            { label: "New Appointment", to: "/appointments", icon: "📅" },
                                            { label: "Patient Records", to: "/patients", icon: "🧑‍⚕️" },
                                            { label: "Lab Orders", to: "/labs/orders", icon: "🧬" },
                                            { label: "AI Diagnosis", to: "/ai/clinical", icon: "🤖" },
                                        ].map(item => (_jsx(Link, { to: item.to, style: { textDecoration: "none" }, children: _jsxs("div", { style: { padding: "10px 12px", borderRadius: 10, background: `${meta.color}08`, border: `1px solid ${meta.color}20`, display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }, children: [_jsx("span", { style: { fontSize: 14 }, children: item.icon }), _jsx("span", { style: { fontSize: 11, fontWeight: 600, color: meta.color }, children: item.label })] }) }, item.to))) })] }) })] })] }) }));
}
