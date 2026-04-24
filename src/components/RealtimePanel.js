import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from "react";
import { useRealtime } from "@/hooks/useRealtime";
const SEVERITY_STYLE = {
    critical: { bg: "rgba(239,68,68,0.12)", color: "#f87171", border: "rgba(239,68,68,0.4)" },
    high: { bg: "rgba(245,158,11,0.10)", color: "#fbbf24", border: "rgba(245,158,11,0.3)" },
    moderate: { bg: "rgba(59,130,246,0.08)", color: "#60a5fa", border: "rgba(59,130,246,0.3)" },
    low: { bg: "rgba(16,185,129,0.08)", color: "#4ade80", border: "rgba(16,185,129,0.3)" },
};
const TYPE_ICON = {
    alert: "🚨", patient: "🧑‍⚕️", lab: "🧬", radiology: "🩻", pharmacy: "💊",
};
export default function RealtimePanel() {
    const { alerts, connected, dismiss, dismissAll } = useRealtime();
    const [open, setOpen] = useState(false);
    const criticalCount = alerts.filter(a => a.severity === "critical").length;
    const hasAlerts = alerts.length > 0;
    return (_jsxs(_Fragment, { children: [_jsxs("div", { style: { position: "relative", display: "inline-block" }, children: [_jsx("button", { onClick: () => setOpen(o => !o), style: {
                            width: 38, height: 38, borderRadius: 10, border: "none",
                            background: hasAlerts ? "rgba(239,68,68,0.15)" : "rgba(255,255,255,0.06)",
                            color: hasAlerts ? "#f87171" : "#94a3b8",
                            cursor: "pointer", fontSize: 17, display: "flex",
                            alignItems: "center", justifyContent: "center",
                            boxShadow: criticalCount > 0 ? "0 0 12px rgba(239,68,68,0.4)" : "none",
                            transition: "all 0.2s",
                        }, children: "\uD83D\uDD14" }), hasAlerts && (_jsx("div", { style: {
                            position: "absolute", top: -4, right: -4,
                            width: 18, height: 18, borderRadius: "50%",
                            background: criticalCount > 0 ? "#ef4444" : "#3b82f6",
                            color: "white", fontSize: 10, fontWeight: 900,
                            display: "flex", alignItems: "center", justifyContent: "center",
                            boxShadow: "0 0 8px rgba(239,68,68,0.6)",
                        }, children: alerts.length > 9 ? "9+" : alerts.length })), _jsx("div", { style: {
                            position: "absolute", bottom: -2, left: -2,
                            width: 8, height: 8, borderRadius: "50%",
                            background: connected ? "#4ade80" : "#64748b",
                            boxShadow: connected ? "0 0 6px #4ade80" : "none",
                            border: "1px solid #020817",
                        } })] }), open && (_jsxs("div", { style: {
                    position: "fixed", top: 60, right: 20, width: 360, zIndex: 1000,
                    background: "linear-gradient(135deg,#0f172a,#1a2540)",
                    border: "1px solid rgba(59,130,246,0.2)",
                    borderRadius: 16, boxShadow: "0 20px 60px rgba(0,0,0,0.6)",
                    overflow: "hidden",
                }, children: [_jsxs("div", { style: {
                            padding: "14px 16px", display: "flex", justifyContent: "space-between",
                            alignItems: "center", borderBottom: "1px solid rgba(255,255,255,0.06)",
                        }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: {
                                            width: 8, height: 8, borderRadius: "50%",
                                            background: connected ? "#4ade80" : "#64748b",
                                            boxShadow: connected ? "0 0 8px #4ade80" : "none",
                                        } }), _jsxs("span", { style: { fontWeight: 700, color: "white", fontSize: 13 }, children: ["Real-time Alerts ", connected ? "(Live)" : "(Offline)"] })] }), _jsxs("div", { style: { display: "flex", gap: 8 }, children: [hasAlerts && (_jsx("button", { onClick: dismissAll, style: {
                                            padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 600,
                                            background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
                                            color: "#f87171", cursor: "pointer",
                                        }, children: "Clear all" })), _jsx("button", { onClick: () => setOpen(false), style: {
                                            width: 24, height: 24, borderRadius: 6, border: "none",
                                            background: "rgba(255,255,255,0.06)", color: "#64748b",
                                            cursor: "pointer", fontSize: 14,
                                        }, children: "\u00D7" })] })] }), _jsx("div", { style: { maxHeight: 400, overflowY: "auto" }, children: alerts.length === 0 ? (_jsxs("div", { style: { padding: 32, textAlign: "center" }, children: [_jsx("div", { style: { fontSize: 32, marginBottom: 8 }, children: "\u2713" }), _jsx("div", { style: { color: "#4ade80", fontSize: 13, fontWeight: 600 }, children: "All systems normal" }), _jsx("div", { style: { color: "#475569", fontSize: 11, marginTop: 4 }, children: connected ? "Monitoring live..." : "Connecting..." })] })) : (alerts.map(alert => {
                            const s = SEVERITY_STYLE[alert.severity] ?? SEVERITY_STYLE.low;
                            return (_jsxs("div", { style: {
                                    padding: "12px 16px", borderBottom: "1px solid rgba(255,255,255,0.04)",
                                    background: s.bg, display: "flex", gap: 10, alignItems: "flex-start",
                                }, children: [_jsx("span", { style: { fontSize: 18, flexShrink: 0 }, children: TYPE_ICON[alert.type] ?? "🔔" }), _jsxs("div", { style: { flex: 1, minWidth: 0 }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 3 }, children: [_jsx("span", { style: {
                                                            fontSize: 10, fontWeight: 800, color: s.color,
                                                            textTransform: "uppercase", letterSpacing: 1,
                                                        }, children: alert.severity }), _jsx("span", { style: { fontSize: 10, color: "#475569" }, children: new Date(alert.timestamp).toLocaleTimeString() })] }), _jsx("div", { style: { color: "#cbd5e1", fontSize: 12, lineHeight: 1.5 }, children: alert.message }), alert.patientId && (_jsxs("div", { style: { color: "#475569", fontSize: 11, marginTop: 3 }, children: ["Patient: ", alert.patientId] }))] }), _jsx("button", { onClick: () => dismiss(alert.id), style: {
                                            width: 20, height: 20, borderRadius: 4, border: "none",
                                            background: "rgba(255,255,255,0.06)", color: "#64748b",
                                            cursor: "pointer", fontSize: 12, flexShrink: 0,
                                        }, children: "\u00D7" })] }, alert.id));
                        })) })] }))] }));
}
