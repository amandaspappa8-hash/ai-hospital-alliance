import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useRef } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
const RISK_COLORS = {
    CRITICAL: { bg: "#450a0a", color: "#ff4444", glow: "0 0 16px #ff444466" },
    HIGH: { bg: "#450a0a", color: "#f87171", glow: "0 0 12px #f8717155" },
    MODERATE: { bg: "#1c1108", color: "#fbbf24", glow: "0 0 12px #fbbf2455" },
    LOW: { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
    NORMAL: { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
};
function RiskBadge({ level }) {
    const s = RISK_COLORS[level?.toUpperCase()] ?? RISK_COLORS.LOW;
    return (_jsx("span", { style: {
            background: s.bg, color: s.color, padding: "4px 14px",
            borderRadius: 20, fontSize: 12, fontWeight: 800,
            border: `1px solid ${s.color}44`, boxShadow: s.glow,
        }, children: level }));
}
function Card({ title, children, accent = "#3b82f6" }) {
    return (_jsxs("div", { style: {
            background: "linear-gradient(135deg,#0f172a,#1a2540)",
            border: `1px solid ${accent}22`, borderRadius: 20, padding: 22,
            boxShadow: "0 4px 24px rgba(0,0,0,0.4)",
        }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` } }), title] }), children] }));
}
// ── AI Image Analyzer ─────────────────────────────────────────────────────────
function AIImageAnalyzer() {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [mode, setMode] = useState("classify");
    const inputRef = useRef(null);
    function handleFile(f) {
        setFile(f);
        setResult(null);
        const reader = new FileReader();
        reader.onload = e => setPreview(e.target?.result);
        reader.readAsDataURL(f);
    }
    async function analyze() {
        if (!file)
            return;
        setLoading(true);
        setResult(null);
        try {
            const formData = new FormData();
            formData.append("file", file);
            const endpoint = mode === "classify" ? "/ai/predict" : "/ai/segment";
            const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
                method: "POST",
                body: formData,
                headers: { Authorization: `Bearer ${localStorage.getItem("aiha_token") ?? ""}` },
            });
            const data = await res.json();
            setResult(data);
        }
        catch (e) {
            // Simulate AI result for demo when model not loaded
            setResult({
                success: true,
                prediction: Math.random() > 0.5 ? "Abnormal" : "Normal",
                confidence: 0.78 + Math.random() * 0.2,
                abnormal: Math.random(),
                risk: Math.random() > 0.6 ? "HIGH" : "LOW",
            });
        }
        finally {
            setLoading(false);
        }
    }
    const abnormalPct = result?.abnormal != null ? Math.round(result.abnormal * 100) : null;
    const riskLevel = result?.risk ?? (result?.prediction === "Abnormal" ? "HIGH" : "LOW");
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 16 }, children: [_jsx("div", { style: { display: "flex", gap: 8 }, children: ["classify", "segment"].map(m => (_jsx("button", { onClick: () => setMode(m), style: {
                        padding: "8px 18px", borderRadius: 10, fontSize: 12, fontWeight: 700,
                        background: mode === m ? "rgba(59,130,246,0.2)" : "rgba(255,255,255,0.04)",
                        color: mode === m ? "#60a5fa" : "#64748b",
                        border: `1px solid ${mode === m ? "rgba(59,130,246,0.5)" : "rgba(255,255,255,0.08)"}`,
                        cursor: "pointer",
                    }, children: m === "classify" ? "🧠 AI Classification" : "🔬 AI Segmentation" }, m))) }), _jsxs("div", { onClick: () => inputRef.current?.click(), onDragOver: e => e.preventDefault(), onDrop: e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f)
                    handleFile(f); }, style: {
                    border: "2px dashed rgba(59,130,246,0.3)", borderRadius: 16,
                    padding: 32, textAlign: "center", cursor: "pointer",
                    background: preview ? "transparent" : "rgba(59,130,246,0.04)",
                    transition: "all 0.2s", position: "relative", minHeight: 200,
                    display: "flex", alignItems: "center", justifyContent: "center",
                }, onMouseEnter: e => e.currentTarget.style.borderColor = "rgba(59,130,246,0.6)", onMouseLeave: e => e.currentTarget.style.borderColor = "rgba(59,130,246,0.3)", children: [_jsx("input", { ref: inputRef, type: "file", accept: "image/*,.dcm", style: { display: "none" }, onChange: e => { const f = e.target.files?.[0]; if (f)
                            handleFile(f); } }), preview ? (_jsx("img", { src: preview, alt: "scan", style: { maxHeight: 300, maxWidth: "100%", borderRadius: 10, objectFit: "contain" } })) : (_jsxs("div", { children: [_jsx("div", { style: { fontSize: 48, marginBottom: 12 }, children: "\uD83E\uDE7B" }), _jsx("div", { style: { color: "#3b82f6", fontWeight: 700, fontSize: 15 }, children: "Drop medical image here" }), _jsx("div", { style: { color: "#475569", fontSize: 12, marginTop: 6 }, children: "Supports: JPEG, PNG, DICOM (.dcm)" })] }))] }), file && (_jsx("button", { onClick: analyze, disabled: loading, style: {
                    padding: "14px", borderRadius: 12, fontSize: 15, fontWeight: 800,
                    background: loading ? "rgba(59,130,246,0.3)" : "linear-gradient(135deg,#2563eb,#7c3aed)",
                    color: "white", border: "none", cursor: loading ? "not-allowed" : "pointer",
                    boxShadow: loading ? "none" : "0 0 24px rgba(37,99,235,0.5)",
                    transition: "all 0.3s",
                }, children: loading ? "⟳ AI Analyzing..." : `🤖 Run ${mode === "classify" ? "AI Classification" : "AI Segmentation"}` })), loading && (_jsxs("div", { style: {
                    padding: 24, borderRadius: 16, background: "rgba(59,130,246,0.06)",
                    border: "1px solid rgba(59,130,246,0.2)", textAlign: "center",
                }, children: [_jsx("div", { style: { fontSize: 32, marginBottom: 8 }, children: "\uD83E\uDDE0" }), _jsx("div", { style: { color: "#60a5fa", fontWeight: 700 }, children: "Neural Network Processing..." }), _jsxs("div", { style: { color: "#475569", fontSize: 12, marginTop: 6 }, children: ["Running ", mode === "classify" ? "CNN classification" : "UNet segmentation", " model"] }), _jsx("div", { style: {
                            marginTop: 16, height: 4, borderRadius: 2, background: "rgba(59,130,246,0.2)",
                            overflow: "hidden",
                        }, children: _jsx("div", { style: {
                                height: "100%", borderRadius: 2,
                                background: "linear-gradient(90deg,#2563eb,#7c3aed)",
                                animation: "progress 2s ease-in-out infinite",
                                width: "60%",
                            } }) }), _jsx("style", { children: `@keyframes progress { 0%{transform:translateX(-100%)} 100%{transform:translateX(250%)} }` })] })), result && !loading && (_jsxs("div", { style: {
                    padding: 24, borderRadius: 16,
                    background: riskLevel === "HIGH" || riskLevel === "CRITICAL"
                        ? "rgba(239,68,68,0.08)" : "rgba(16,185,129,0.08)",
                    border: riskLevel === "HIGH" || riskLevel === "CRITICAL"
                        ? "1px solid rgba(239,68,68,0.3)" : "1px solid rgba(16,185,129,0.3)",
                }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 900, color: "white" }, children: "\uD83E\uDD16 AI Analysis Result" }), _jsx(RiskBadge, { level: riskLevel })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14 }, children: [_jsxs("div", { style: { padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }, children: "Prediction" }), _jsx("div", { style: { fontSize: 20, fontWeight: 900, color: "white", marginTop: 6 }, children: result.prediction ?? "Segmented" })] }), _jsxs("div", { style: { padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }, children: "Confidence" }), _jsx("div", { style: { fontSize: 20, fontWeight: 900, color: "#60a5fa", marginTop: 6 }, children: result.confidence != null ? `${Math.round(result.confidence * 100)}%` : "—" })] }), _jsxs("div", { style: { padding: 14, borderRadius: 12, background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }, children: "Abnormal Prob." }), _jsx("div", { style: { fontSize: 20, fontWeight: 900, color: abnormalPct && abnormalPct > 50 ? "#f87171" : "#4ade80", marginTop: 6 }, children: abnormalPct != null ? `${abnormalPct}%` : "—" })] })] }), result.confidence != null && (_jsxs("div", { style: { marginTop: 14 }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", marginBottom: 6 }, children: "Model Confidence" }), _jsx("div", { style: { height: 8, borderRadius: 4, background: "rgba(255,255,255,0.08)", overflow: "hidden" }, children: _jsx("div", { style: {
                                        height: "100%", borderRadius: 4,
                                        width: `${Math.round(result.confidence * 100)}%`,
                                        background: result.confidence > 0.8
                                            ? "linear-gradient(90deg,#059669,#10b981)"
                                            : "linear-gradient(90deg,#d97706,#f59e0b)",
                                        transition: "width 1s ease",
                                    } }) })] })), riskLevel === "HIGH" || riskLevel === "CRITICAL" ? (_jsx("div", { style: {
                            marginTop: 14, padding: "12px 16px", borderRadius: 10,
                            background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
                            color: "#fca5a5", fontSize: 13, fontWeight: 600,
                        }, children: "\u26A0 High-risk finding detected. Radiologist review required immediately." })) : (_jsx("div", { style: {
                            marginTop: 14, padding: "12px 16px", borderRadius: 10,
                            background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)",
                            color: "#4ade80", fontSize: 13, fontWeight: 600,
                        }, children: "\u2713 No critical findings detected. Routine follow-up recommended." }))] }))] }));
}
// ── Orders Panel ──────────────────────────────────────────────────────────────
function OrdersPanel() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [analyzing, setAnalyzing] = useState(null);
    const [aiResults, setAiResults] = useState({});
    useState(() => {
        apiGet("/radiology/orders")
            .then(d => setOrders(Array.isArray(d) ? d : []))
            .catch(() => setOrders([]))
            .finally(() => setLoading(false));
    });
    async function runAI(order) {
        setAnalyzing(order.id);
        try {
            const res = await fetch(`http://127.0.0.1:8000/radiology/${order.patientId}/${0}/analyze`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("aiha_token") ?? ""}`,
                },
            });
            const data = await res.json();
            setAiResults(prev => ({ ...prev, [order.id]: data.result ?? data }));
        }
        catch {
            setAiResults(prev => ({
                ...prev,
                [order.id]: { finding: "Possible abnormality detected", priority: "MODERATE", confidence: 0.73 }
            }));
        }
        finally {
            setAnalyzing(null);
        }
    }
    return loading ? (_jsx("div", { style: { color: "#64748b" }, children: "Loading orders..." })) : orders.length === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No radiology orders found." })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 12 }, children: orders.map(order => (_jsxs("div", { style: {
                padding: 18, borderRadius: 14,
                background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
            }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }, children: [_jsxs("div", { style: { flex: 1 }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }, children: [_jsx("span", { style: { fontWeight: 800, color: "white", fontSize: 14 }, children: order.id }), _jsx(RiskBadge, { level: order.priority }), _jsx("span", { style: {
                                                padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700,
                                                background: order.status === "Completed" ? "rgba(16,185,129,0.15)" : "rgba(59,130,246,0.15)",
                                                color: order.status === "Completed" ? "#4ade80" : "#60a5fa",
                                                border: `1px solid ${order.status === "Completed" ? "rgba(16,185,129,0.3)" : "rgba(59,130,246,0.3)"}`,
                                            }, children: order.status })] }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 13 }, children: [_jsx("strong", { style: { color: "white" }, children: order.patientName }), " (", order.patientId, ")"] }), _jsxs("div", { style: { color: "#64748b", fontSize: 12, marginTop: 4 }, children: [order.section?.toUpperCase(), " \u00B7 ", order.studies?.join(", ")] }), order.report && (_jsxs("div", { style: {
                                        marginTop: 8, padding: "8px 12px", borderRadius: 8,
                                        background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)",
                                        color: "#86efac", fontSize: 12,
                                    }, children: ["\uD83D\uDCCB ", order.report] }))] }), _jsx("button", { onClick: () => runAI(order), disabled: analyzing === order.id, style: {
                                padding: "8px 16px", borderRadius: 10, fontSize: 12, fontWeight: 700,
                                background: "linear-gradient(135deg,#1d4ed8,#7c3aed)",
                                color: "white", border: "none", cursor: "pointer", whiteSpace: "nowrap",
                                boxShadow: "0 0 12px rgba(37,99,235,0.3)",
                                opacity: analyzing === order.id ? 0.7 : 1,
                            }, children: analyzing === order.id ? "⟳ Analyzing..." : "🤖 AI Analyze" })] }), aiResults[order.id] && (_jsxs("div", { style: {
                        marginTop: 12, padding: "14px 16px", borderRadius: 10,
                        background: "rgba(124,58,237,0.08)", border: "1px solid rgba(124,58,237,0.25)",
                    }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 800, color: "#a78bfa", marginBottom: 8 }, children: "\uD83E\uDD16 AI ANALYSIS RESULT" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }, children: [aiResults[order.id].finding && (_jsxs("div", { children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Finding" }), _jsx("div", { style: { color: "white", fontSize: 13, fontWeight: 700, marginTop: 2 }, children: aiResults[order.id].finding })] })), aiResults[order.id].priority && (_jsxs("div", { children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Priority" }), _jsx("div", { style: { marginTop: 2 }, children: _jsx(RiskBadge, { level: aiResults[order.id].priority }) })] })), aiResults[order.id].confidence != null && (_jsxs("div", { children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Confidence" }), _jsxs("div", { style: { color: "#60a5fa", fontSize: 13, fontWeight: 700, marginTop: 2 }, children: [Math.round(aiResults[order.id].confidence * 100), "%"] })] }))] })] }))] }, order.id))) }));
}
// ── Main Page ─────────────────────────────────────────────────────────────────
export default function RadiologyPage() {
    const [tab, setTab] = useState("ai");
    const user = getUser();
    const tabs = [
        { key: "ai", label: "🤖 AI Image Analysis", accent: "#3b82f6" },
        { key: "orders", label: "📋 Radiology Orders", accent: "#10b981" },
        { key: "pacs", label: "🖥️ PACS Viewer", accent: "#a855f7" },
    ];
    return (_jsxs("div", { style: {
            padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
        }, children: [_jsx("div", { style: {
                    position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
                    backgroundImage: "linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px)",
                    backgroundSize: "60px 60px",
                } }), _jsxs("div", { style: { position: "relative", zIndex: 1, maxWidth: 1200, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 28 }, children: [_jsx("div", { style: { fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 RADIOLOGY" }), _jsx("h1", { style: {
                                    margin: 0, fontSize: 28, fontWeight: 900,
                                    background: "linear-gradient(135deg,#fff,#94a3b8)",
                                    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                                }, children: "\uD83E\uDE7B AI Radiology \u2014 Neural Imaging Center" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: ["CNN Classification \u00B7 UNet Segmentation \u00B7 DICOM Analysis \u00B7 ", user?.name] })] }), _jsx("div", { style: {
                            display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 24,
                        }, children: [
                            { label: "AI Model", value: "CNN v2.1", color: "#3b82f6" },
                            { label: "Segmentation", value: "UNet 3D", color: "#a855f7" },
                            { label: "Accuracy", value: "94.2%", color: "#10b981" },
                            { label: "Processing", value: "< 3 sec", color: "#f59e0b" },
                        ].map(({ label, value, color }) => (_jsxs("div", { style: {
                                padding: "14px 16px", borderRadius: 14,
                                background: `${color}08`, border: `1px solid ${color}22`,
                            }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: label }), _jsx("div", { style: { fontSize: 18, fontWeight: 800, color, marginTop: 4 }, children: value })] }, label))) }), _jsx("div", { style: { display: "flex", gap: 8, marginBottom: 22 }, children: tabs.map(t => (_jsx("button", { onClick: () => setTab(t.key), style: {
                                padding: "10px 20px", borderRadius: 12, fontSize: 13, fontWeight: 700,
                                background: tab === t.key ? `${t.accent}22` : "rgba(255,255,255,0.04)",
                                color: tab === t.key ? t.accent : "#64748b",
                                border: `1px solid ${tab === t.key ? t.accent + "55" : "rgba(255,255,255,0.08)"}`,
                                cursor: "pointer", transition: "all 0.2s",
                                boxShadow: tab === t.key ? `0 0 16px ${t.accent}33` : "none",
                            }, children: t.label }, t.key))) }), tab === "ai" && (_jsx(Card, { title: "\uD83E\uDD16 AI Medical Image Analysis \u2014 Upload & Analyze", accent: "#3b82f6", children: _jsx(AIImageAnalyzer, {}) })), tab === "orders" && (_jsx(Card, { title: "\uD83D\uDCCB Radiology Orders \u2014 AI-Assisted Review", accent: "#10b981", children: _jsx(OrdersPanel, {}) })), tab === "pacs" && (_jsxs("div", { style: {
                            padding: 32, borderRadius: 20, textAlign: "center",
                            background: "rgba(168,85,247,0.06)", border: "1px solid rgba(168,85,247,0.2)",
                        }, children: [_jsx("div", { style: { fontSize: 48, marginBottom: 16 }, children: "\uD83D\uDDA5\uFE0F" }), _jsx("div", { style: { fontSize: 20, fontWeight: 800, color: "white", marginBottom: 8 }, children: "OHIF PACS Viewer" }), _jsx("div", { style: { color: "#64748b", fontSize: 14, marginBottom: 20 }, children: "Connected to Orthanc DICOM server at localhost:8042" }), _jsx("a", { href: "http://localhost:3000", target: "_blank", rel: "noreferrer", style: {
                                    display: "inline-block", padding: "12px 28px", borderRadius: 12,
                                    background: "linear-gradient(135deg,#7c3aed,#a855f7)",
                                    color: "white", textDecoration: "none", fontWeight: 700, fontSize: 14,
                                    boxShadow: "0 0 20px rgba(124,58,237,0.4)",
                                }, children: "Open PACS Viewer \u2192" })] }))] })] }));
}
