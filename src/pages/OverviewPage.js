import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
export default function OverviewPage() {
    const user = getUser();
    const [stats, setStats] = useState({ patients: 0, doctors: 0, appointments: 0, alerts: 0 });
    useEffect(() => {
        Promise.all([
            apiGet("/patients").catch(() => []),
            apiGet("/doctors/summary").catch(() => []),
            apiGet("/appointments").catch(() => []),
            apiGet("/alerts").catch(() => []),
        ]).then(([p, d, a, al]) => setStats({
            patients: p.length, doctors: d.length,
            appointments: a.length, alerts: al.length,
        }));
    }, []);
    const sections = [
        { title: "Patients", value: stats.patients, icon: "🧑‍⚕️", color: "#3b82f6", to: "/patients" },
        { title: "Doctors", value: stats.doctors, icon: "👨‍⚕️", color: "#10b981", to: "/doctors" },
        { title: "Appointments", value: stats.appointments, icon: "📅", color: "#a855f7", to: "/appointments" },
        { title: "Alerts", value: stats.alerts, icon: "🔔", color: "#ef4444", to: "/alerts" },
    ];
    return (_jsx("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: _jsxs("div", { style: { maxWidth: 1200, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 28 }, children: [_jsx("div", { style: { fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 OVERVIEW" }), _jsx("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#94a3b8)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }, children: "\uD83D\uDCCA System Overview" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: [user?.name, " \u00B7 ", user?.role, " \u00B7 ", new Date().toLocaleDateString()] })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 16, marginBottom: 28 }, children: sections.map(s => (_jsx(Link, { to: s.to, style: { textDecoration: "none" }, children: _jsxs("div", { style: { padding: "22px 20px", borderRadius: 18, background: `${s.color}08`, border: `1px solid ${s.color}22`, cursor: "pointer", transition: "all 0.2s" }, onMouseEnter: e => e.currentTarget.style.transform = "translateY(-2px)", onMouseLeave: e => e.currentTarget.style.transform = "translateY(0)", children: [_jsx("div", { style: { fontSize: 28, marginBottom: 8 }, children: s.icon }), _jsx("div", { style: { fontSize: 32, fontWeight: 900, color: s.color }, children: s.value }), _jsx("div", { style: { fontSize: 13, color: "#94a3b8", marginTop: 4 }, children: s.title })] }) }, s.to))) }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }, children: [
                        { title: "Radiology", icon: "🩻", color: "#f97316", to: "/radiology", desc: "AI Image Analysis · PACS · CT/MRI" },
                        { title: "Laboratory", icon: "🧬", color: "#10b981", to: "/labs", desc: "AI Interpreter · 50,000+ References" },
                        { title: "Pharmacy", icon: "💊", color: "#f43f5e", to: "/pharmacy", desc: "FDA Database · RxNorm · MAR" },
                        { title: "AI Engine", icon: "🤖", color: "#6366f1", to: "/ai-routing", desc: "Clinical Decision · Diagnosis AI" },
                        { title: "Specialties", icon: "🏥", color: "#8b5cf6", to: "/specialties", desc: "6 Departments · Cardiology · ICU" },
                        { title: "Reports", icon: "📄", color: "#f59e0b", to: "/reports", desc: "Clinical Reports · Auto-generated" },
                    ].map(item => (_jsx(Link, { to: item.to, style: { textDecoration: "none" }, children: _jsxs("div", { style: { padding: "20px 22px", borderRadius: 18, background: `${item.color}06`, border: `1px solid ${item.color}20`, cursor: "pointer", transition: "all 0.2s" }, onMouseEnter: e => { e.currentTarget.style.background = `${item.color}12`; e.currentTarget.style.transform = "translateY(-2px)"; }, onMouseLeave: e => { e.currentTarget.style.background = `${item.color}06`; e.currentTarget.style.transform = "translateY(0)"; }, children: [_jsx("div", { style: { fontSize: 26, marginBottom: 8 }, children: item.icon }), _jsx("div", { style: { fontWeight: 800, color: "white", fontSize: 16, marginBottom: 6 }, children: item.title }), _jsx("div", { style: { color: "#64748b", fontSize: 12, lineHeight: 1.5 }, children: item.desc })] }) }, item.to))) })] }) }));
}
