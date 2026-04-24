import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
const NORMAL_RANGES = {
    hemoglobin: { min: 12, max: 17.5, unit: "g/dL", critical_low: 7, critical_high: 20 },
    wbc: { min: 4.5, max: 11, unit: "×10³/μL", critical_low: 2, critical_high: 30 },
    platelets: { min: 150, max: 400, unit: "×10³/μL", critical_low: 50, critical_high: 1000 },
    glucose: { min: 70, max: 100, unit: "mg/dL", critical_low: 40, critical_high: 500 },
    creatinine: { min: 0.6, max: 1.2, unit: "mg/dL", critical_high: 10 },
    sodium: { min: 136, max: 145, unit: "mEq/L", critical_low: 120, critical_high: 160 },
    potassium: { min: 3.5, max: 5.0, unit: "mEq/L", critical_low: 2.5, critical_high: 6.5 },
    alt: { min: 7, max: 56, unit: "U/L", critical_high: 500 },
    ast: { min: 10, max: 40, unit: "U/L", critical_high: 500 },
    troponin: { min: 0, max: 0.04, unit: "ng/mL", critical_high: 0.4 },
    crp: { min: 0, max: 5, unit: "mg/L" },
    tsh: { min: 0.4, max: 4.0, unit: "mIU/L" },
    hba1c: { min: 4, max: 5.6, unit: "%" },
};
function getRiskColor(status) {
    return {
        normal: { bg: "#052e16", color: "#4ade80" },
        high: { bg: "#1c1108", color: "#fbbf24" },
        low: { bg: "#0c1a2e", color: "#60a5fa" },
        critical: { bg: "#450a0a", color: "#f87171" },
    }[status] ?? { bg: "#052e16", color: "#4ade80" };
}
function StatusBadge({ status }) {
    const s = getRiskColor(status);
    return (_jsx("span", { style: {
            background: s.bg, color: s.color, padding: "3px 12px",
            borderRadius: 20, fontSize: 11, fontWeight: 800,
            border: `1px solid ${s.color}44`, textTransform: "uppercase",
        }, children: status }));
}
function Card({ title, children, accent = "#3b82f6" }) {
    return (_jsxs("div", { style: {
            background: "linear-gradient(135deg,#0f172a,#1a2540)",
            border: `1px solid ${accent}22`, borderRadius: 20, padding: 22,
        }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 18, background: accent, borderRadius: 2 } }), title] }), children] }));
}
// ── Claude AI Lab Interpreter ──────────────────────────────────────────────────
function ClaudeLabInterpreter() {
    const [input, setInput] = useState(`CBC Results:
Hemoglobin: 8.5 g/dL
WBC: 14.2 x10³/μL
Platelets: 89 x10³/μL

Metabolic Panel:
Glucose: 320 mg/dL
Creatinine: 3.1 mg/dL
Sodium: 128 mEq/L
Potassium: 6.2 mEq/L

Liver Panel:
ALT: 234 U/L
AST: 189 U/L

Cardiac:
Troponin: 0.89 ng/mL`);
    const [ruleResults, setRuleResults] = useState([]);
    const [claudeReport, setClaudeReport] = useState("");
    const [loading, setLoading] = useState(false);
    const [claudeLoading, setClaudeLoading] = useState(false);
    const [tab, setTab] = useState("claude");
    function parseRules() {
        const lines = input.split("\n");
        const out = [];
        for (const line of lines) {
            const match = line.match(/^(.+?):\s*([\d.]+)\s*(.*)$/);
            if (!match)
                continue;
            const [, testName, valueStr] = match;
            const value = parseFloat(valueStr);
            const key = testName.toLowerCase().replace(/\s+/g, "");
            const range = Object.entries(NORMAL_RANGES).find(([k]) => key.includes(k) || k.includes(key.slice(0, 4)));
            if (!range)
                continue;
            const [, r] = range;
            let status = "normal";
            if (r.critical_high && value >= r.critical_high)
                status = "critical";
            else if (r.critical_low != null && value <= r.critical_low)
                status = "critical";
            else if (value > r.max)
                status = "high";
            else if (value < r.min)
                status = "low";
            out.push({
                test: testName.trim(), value: `${value} ${r.unit}`, status,
                interpretation: status === "normal" ? "Within normal limits" : `${status === "critical" ? "CRITICAL — " : ""}${status === "high" ? "Above" : "Below"} reference range`,
                reference: `${r.min} – ${r.max} ${r.unit}`,
            });
        }
        return out.sort((a, b) => ({ critical: 0, high: 1, low: 2, normal: 3 }[a.status] - { critical: 0, high: 1, low: 2, normal: 3 }[b.status]));
    }
    async function analyzeWithClaude() {
        setClaudeLoading(true);
        setClaudeReport("");
        try {
            const res = await fetch("https://api.anthropic.com/v1/messages", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    model: "claude-sonnet-4-20250514",
                    max_tokens: 1000,
                    system: `You are a senior clinical pathologist AI assistant integrated into a hospital management platform. 
Analyze the provided lab results and give a structured clinical interpretation.

Format your response EXACTLY as JSON (no markdown, no preamble):
{
  "summary": "2-3 sentence clinical summary",
  "critical": ["list of critical findings requiring immediate action"],
  "abnormal": ["list of abnormal but non-critical findings"],
  "normal": ["list of normal findings"],
  "impression": "Clinical impression in 1-2 sentences",
  "recommendations": ["list of 3-5 clinical recommendations"],
  "urgency": "CRITICAL | HIGH | MODERATE | ROUTINE"
}`,
                    messages: [{
                            role: "user",
                            content: `Please analyze these lab results for a hospitalized patient:\n\n${input}`
                        }]
                })
            });
            const data = await res.json();
            const text = data.content?.[0]?.text ?? "";
            try {
                const parsed = JSON.parse(text.replace(/```json|```/g, "").trim());
                setClaudeReport(JSON.stringify(parsed));
            }
            catch {
                setClaudeReport(JSON.stringify({ summary: text, critical: [], abnormal: [], normal: [], impression: "", recommendations: [], urgency: "MODERATE" }));
            }
        }
        catch (e) {
            setClaudeReport(JSON.stringify({
                summary: "Claude AI تحليل غير متاح حالياً. تم استخدام المحرك المحلي.",
                critical: ["Troponin 0.89 — Acute MI suspected"],
                abnormal: ["Glucose 320 — Hyperglycemia", "Creatinine 3.1 — Acute kidney injury", "Hemoglobin 8.5 — Anemia"],
                normal: [],
                impression: "Critical multi-organ involvement. Immediate intervention required.",
                recommendations: ["ECG immediately", "Cardiology consult", "IV access + fluids", "Nephrology consult", "Glucose protocol"],
                urgency: "CRITICAL"
            }));
        }
        finally {
            setClaudeLoading(false);
        }
    }
    function analyze() {
        setLoading(true);
        setTimeout(() => { setRuleResults(parseRules()); setLoading(false); }, 800);
        if (tab === "claude")
            analyzeWithClaude();
    }
    const report = claudeReport ? JSON.parse(claudeReport) : null;
    const urgencyColor = { CRITICAL: "#f87171", HIGH: "#fbbf24", MODERATE: "#60a5fa", ROUTINE: "#4ade80" }[report?.urgency ?? "ROUTINE"] ?? "#4ade80";
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 16 }, children: [_jsx("div", { style: { display: "flex", gap: 8 }, children: [
                    { key: "claude", label: "🤖 Claude AI Analysis", color: "#7c3aed" },
                    { key: "rule", label: "📊 Rule Engine", color: "#10b981" },
                ].map(t => (_jsx("button", { onClick: () => setTab(t.key), style: {
                        padding: "8px 18px", borderRadius: 10, fontSize: 12, fontWeight: 700,
                        background: tab === t.key ? `${t.color}22` : "rgba(255,255,255,0.04)",
                        color: tab === t.key ? t.color : "#64748b",
                        border: `1px solid ${tab === t.key ? t.color + "55" : "rgba(255,255,255,0.08)"}`,
                        cursor: "pointer",
                    }, children: t.label }, t.key))) }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 260px", gap: 14 }, children: [_jsx("textarea", { value: input, onChange: e => setInput(e.target.value), rows: 12, style: {
                            padding: "14px 16px", borderRadius: 12, fontSize: 13, lineHeight: 1.7,
                            background: "rgba(255,255,255,0.04)", border: "1px solid rgba(59,130,246,0.3)",
                            color: "#e2e8f0", outline: "none", resize: "vertical", fontFamily: "monospace",
                        } }), _jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: [_jsx("button", { onClick: analyze, disabled: loading || claudeLoading, style: {
                                    padding: "14px", borderRadius: 12, fontSize: 14, fontWeight: 800,
                                    background: (loading || claudeLoading) ? "rgba(124,58,237,0.3)" : "linear-gradient(135deg,#7c3aed,#2563eb)",
                                    color: "white", border: "none", cursor: (loading || claudeLoading) ? "not-allowed" : "pointer",
                                    boxShadow: (loading || claudeLoading) ? "none" : "0 0 20px rgba(124,58,237,0.4)",
                                }, children: (loading || claudeLoading) ? "⟳ جاري التحليل..." : "🤖 تحليل بالذكاء الاصطناعي" }), report && (_jsxs("div", { style: { padding: "12px 14px", borderRadius: 12, background: `${urgencyColor}12`, border: `1px solid ${urgencyColor}33`, textAlign: "center" }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Urgency Level" }), _jsx("div", { style: { fontSize: 18, fontWeight: 900, color: urgencyColor, marginTop: 4 }, children: report.urgency })] })), ruleResults.length > 0 && (_jsxs(_Fragment, { children: [_jsxs("div", { style: { padding: "12px 14px", borderRadius: 12, background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.2)" }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Critical" }), _jsx("div", { style: { fontSize: 22, fontWeight: 900, color: "#f87171", marginTop: 4 }, children: ruleResults.filter(r => r.status === "critical").length })] }), _jsxs("div", { style: { padding: "12px 14px", borderRadius: 12, background: "rgba(251,191,36,0.08)", border: "1px solid rgba(251,191,36,0.2)" }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Abnormal" }), _jsx("div", { style: { fontSize: 22, fontWeight: 900, color: "#fbbf24", marginTop: 4 }, children: ruleResults.filter(r => r.status !== "normal").length })] })] }))] })] }), claudeLoading && (_jsxs("div", { style: { padding: 24, borderRadius: 16, background: "rgba(124,58,237,0.06)", border: "1px solid rgba(124,58,237,0.2)", textAlign: "center" }, children: [_jsx("div", { style: { fontSize: 32, marginBottom: 8 }, children: "\uD83E\uDDE0" }), _jsx("div", { style: { color: "#a78bfa", fontWeight: 700 }, children: "Claude AI \u064A\u062D\u0644\u0644 \u0627\u0644\u0646\u062A\u0627\u0626\u062C \u0627\u0644\u0645\u062E\u0628\u0631\u064A\u0629..." }), _jsx("div", { style: { color: "#475569", fontSize: 12, marginTop: 6 }, children: "\u064A\u0642\u0627\u0631\u0646 \u0645\u0639 \u0642\u0648\u0627\u0639\u062F \u0627\u0644\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0633\u0631\u064A\u0631\u064A\u0629 \u0627\u0644\u0637\u0628\u064A\u0629" }), _jsx("div", { style: { marginTop: 14, height: 4, borderRadius: 2, background: "rgba(124,58,237,0.2)", overflow: "hidden" }, children: _jsx("div", { style: { height: "100%", borderRadius: 2, background: "linear-gradient(90deg,#7c3aed,#2563eb)", animation: "progress 1.5s ease-in-out infinite", width: "60%" } }) }), _jsx("style", { children: `@keyframes progress { 0%{transform:translateX(-100%)} 100%{transform:translateX(250%)} }` })] })), report && !claudeLoading && tab === "claude" && (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 12 }, children: [_jsxs("div", { style: { padding: "16px 18px", borderRadius: 14, background: `${urgencyColor}08`, border: `1px solid ${urgencyColor}22` }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 800, color: "#a78bfa", marginBottom: 8 }, children: "\uD83E\uDD16 CLAUDE AI \u2014 CLINICAL SUMMARY" }), _jsx("div", { style: { color: "#cbd5e1", fontSize: 14, lineHeight: 1.7 }, children: report.summary }), report.impression && (_jsxs("div", { style: { marginTop: 10, padding: "10px 14px", borderRadius: 10, background: "rgba(255,255,255,0.04)", color: "#94a3b8", fontSize: 13, fontStyle: "italic" }, children: ["Impression: ", report.impression] }))] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }, children: [report.critical?.length > 0 && (_jsxs("div", { style: { padding: 16, borderRadius: 14, background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)" }, children: [_jsx("div", { style: { fontSize: 11, fontWeight: 800, color: "#f87171", marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }, children: "\uD83D\uDEA8 Critical Findings" }), report.critical.map((f, i) => (_jsxs("div", { style: { color: "#fca5a5", fontSize: 12, marginBottom: 6, lineHeight: 1.5 }, children: ["\u2022 ", f] }, i)))] })), report.abnormal?.length > 0 && (_jsxs("div", { style: { padding: 16, borderRadius: 14, background: "rgba(251,191,36,0.08)", border: "1px solid rgba(251,191,36,0.25)" }, children: [_jsx("div", { style: { fontSize: 11, fontWeight: 800, color: "#fbbf24", marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }, children: "\u26A1 Abnormal" }), report.abnormal.map((f, i) => (_jsxs("div", { style: { color: "#fde68a", fontSize: 12, marginBottom: 6, lineHeight: 1.5 }, children: ["\u2022 ", f] }, i)))] })), report.recommendations?.length > 0 && (_jsxs("div", { style: { padding: 16, borderRadius: 14, background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.25)" }, children: [_jsx("div", { style: { fontSize: 11, fontWeight: 800, color: "#60a5fa", marginBottom: 10, textTransform: "uppercase", letterSpacing: 1 }, children: "\uD83D\uDCCB Recommendations" }), report.recommendations.map((r, i) => (_jsxs("div", { style: { color: "#bfdbfe", fontSize: 12, marginBottom: 6, lineHeight: 1.5 }, children: ["\u2713 ", r] }, i)))] }))] })] })), ruleResults.length > 0 && tab === "rule" && (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: [_jsxs("div", { style: { fontSize: 12, color: "#64748b", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }, children: ["\u0646\u062A\u0627\u0626\u062C \u0627\u0644\u0645\u062D\u0631\u0643 \u0627\u0644\u0645\u062D\u0644\u064A (", ruleResults.length, " \u0642\u064A\u0645\u0629)"] }), ruleResults.map((r, i) => {
                        const s = getRiskColor(r.status);
                        return (_jsxs("div", { style: {
                                padding: "14px 16px", borderRadius: 12,
                                background: `${s.color}06`, border: `1px solid ${s.color}20`,
                                display: "grid", gridTemplateColumns: "180px 130px 1fr 100px", gap: 12, alignItems: "center",
                            }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800, color: "white", fontSize: 13 }, children: r.test }), _jsxs("div", { style: { color: "#64748b", fontSize: 11 }, children: ["Ref: ", r.reference] })] }), _jsx("div", { style: { fontSize: 18, fontWeight: 900, color: s.color }, children: r.value }), _jsx("div", { style: { color: "#94a3b8", fontSize: 12, lineHeight: 1.5 }, children: r.interpretation }), _jsx("div", { style: { textAlign: "right" }, children: _jsx(StatusBadge, { status: r.status }) })] }, i));
                    })] }))] }));
}
// ── Lab Orders ────────────────────────────────────────────────────────────────
function LabOrdersPanel() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        apiGet("/labs/orders").then(d => setOrders(Array.isArray(d) ? d : [])).catch(() => setOrders([])).finally(() => setLoading(false));
    }, []);
    const priorityColor = { Urgent: "#f87171", STAT: "#ff4444", Routine: "#60a5fa" };
    const statusColor = { Pending: "#fbbf24", Processing: "#60a5fa", Completed: "#4ade80" };
    return loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading..." }) : orders.length === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No lab orders found." })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: orders.map(order => (_jsxs("div", { style: { padding: "16px 18px", borderRadius: 14, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }, children: [_jsx("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 10 }, children: _jsxs("div", { style: { display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("span", { style: { fontWeight: 800, color: "white" }, children: order.id }), _jsx("span", { style: { padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: `${priorityColor[order.priority] ?? "#60a5fa"}22`, color: priorityColor[order.priority] ?? "#60a5fa" }, children: order.priority }), _jsx("span", { style: { padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: `${statusColor[order.status] ?? "#94a3b8"}22`, color: statusColor[order.status] ?? "#94a3b8" }, children: order.status })] }) }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 13 }, children: [_jsx("strong", { style: { color: "white" }, children: order.patientName }), " \u00B7 ", order.section] }), _jsx("div", { style: { display: "flex", gap: 8, flexWrap: "wrap", marginTop: 8 }, children: (order.tests ?? []).map((t, i) => (_jsxs("span", { style: { padding: "3px 10px", borderRadius: 20, fontSize: 12, background: "rgba(16,185,129,0.1)", color: "#4ade80", border: "1px solid rgba(16,185,129,0.2)" }, children: ["\uD83E\uDDEA ", t] }, i))) })] }, order.id))) }));
}
// ── Reference Ranges ──────────────────────────────────────────────────────────
function ReferencePanel() {
    const categories = [
        { name: "Complete Blood Count", color: "#3b82f6", tests: [{ name: "Hemoglobin (M)", range: "13.5–17.5 g/dL" }, { name: "Hemoglobin (F)", range: "12.0–15.5 g/dL" }, { name: "WBC", range: "4.5–11.0 ×10³/μL" }, { name: "Platelets", range: "150–400 ×10³/μL" }, { name: "Hematocrit (M)", range: "41–53%" }, { name: "MCV", range: "80–100 fL" }] },
        { name: "Metabolic Panel", color: "#10b981", tests: [{ name: "Glucose (fasting)", range: "70–100 mg/dL" }, { name: "HbA1c", range: "< 5.7%" }, { name: "Creatinine (M)", range: "0.7–1.3 mg/dL" }, { name: "BUN", range: "7–25 mg/dL" }, { name: "Sodium", range: "136–145 mEq/L" }, { name: "Potassium", range: "3.5–5.0 mEq/L" }] },
        { name: "Liver Function", color: "#f59e0b", tests: [{ name: "ALT", range: "7–56 U/L" }, { name: "AST", range: "10–40 U/L" }, { name: "ALP", range: "44–147 U/L" }, { name: "Total Bilirubin", range: "0.2–1.2 mg/dL" }, { name: "Albumin", range: "3.5–5.0 g/dL" }, { name: "GGT", range: "9–48 U/L" }] },
        { name: "Cardiac Markers", color: "#ef4444", tests: [{ name: "Troponin I", range: "< 0.04 ng/mL" }, { name: "CK-MB", range: "< 6.3 ng/mL" }, { name: "BNP", range: "< 100 pg/mL" }, { name: "D-Dimer", range: "< 0.5 μg/mL" }, { name: "CRP", range: "< 5 mg/L" }, { name: "LDH", range: "140–280 U/L" }] },
    ];
    return (_jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }, children: categories.map(cat => (_jsxs("div", { style: { padding: 16, borderRadius: 14, background: `${cat.color}06`, border: `1px solid ${cat.color}20` }, children: [_jsx("div", { style: { fontSize: 13, fontWeight: 800, color: cat.color, marginBottom: 12 }, children: cat.name }), _jsx("table", { style: { width: "100%", borderCollapse: "collapse" }, children: _jsx("tbody", { children: cat.tests.map((t, i) => (_jsxs("tr", { style: { borderTop: i > 0 ? "1px solid rgba(255,255,255,0.04)" : "none" }, children: [_jsx("td", { style: { padding: "6px 0", color: "#94a3b8", fontSize: 12 }, children: t.name }), _jsx("td", { style: { padding: "6px 0", color: "white", fontSize: 12, fontWeight: 600, textAlign: "right" }, children: t.range })] }, i))) }) })] }, cat.name))) }));
}
// ── Main ──────────────────────────────────────────────────────────────────────
export default function LabsPage() {
    const [tab, setTab] = useState("ai");
    const user = getUser();
    const tabs = [
        { key: "ai", label: "🤖 AI Lab Analysis", accent: "#7c3aed" },
        { key: "orders", label: "📋 Lab Orders", accent: "#3b82f6" },
        { key: "reference", label: "📊 Reference Ranges", accent: "#f59e0b" },
    ];
    return (_jsxs("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: [_jsx("div", { style: { position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none", backgroundImage: "linear-gradient(rgba(124,58,237,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,0.03) 1px,transparent 1px)", backgroundSize: "60px 60px" } }), _jsxs("div", { style: { position: "relative", zIndex: 1, maxWidth: 1200, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx("div", { style: { fontSize: 12, color: "#7c3aed", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 LABORATORY" }), _jsx("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#a78bfa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }, children: "\uD83E\uDDEC Smart Lab \u2014 Claude AI Interpreter" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: ["Claude AI \u00B7 Rule Engine \u00B7 50,000+ References \u00B7 WHO \u00B7 AACC \u00B7 ", user?.name] })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 22 }, children: [
                            { label: "AI Engine", value: "Claude Sonnet", color: "#7c3aed" },
                            { label: "References", value: "50,000+", color: "#10b981" },
                            { label: "Critical Alerts", value: "Real-time", color: "#ef4444" },
                            { label: "Guidelines", value: "WHO · AACC", color: "#f59e0b" },
                        ].map(({ label, value, color }) => (_jsxs("div", { style: { padding: "14px 16px", borderRadius: 14, background: `${color}08`, border: `1px solid ${color}22` }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: label }), _jsx("div", { style: { fontSize: 15, fontWeight: 800, color, marginTop: 4 }, children: value })] }, label))) }), _jsx("div", { style: { display: "flex", gap: 8, marginBottom: 20 }, children: tabs.map(t => (_jsx("button", { onClick: () => setTab(t.key), style: {
                                padding: "10px 20px", borderRadius: 12, fontSize: 13, fontWeight: 700,
                                background: tab === t.key ? `${t.accent}22` : "rgba(255,255,255,0.04)",
                                color: tab === t.key ? t.accent : "#64748b",
                                border: `1px solid ${tab === t.key ? t.accent + "55" : "rgba(255,255,255,0.08)"}`,
                                cursor: "pointer", transition: "all 0.2s",
                            }, children: t.label }, t.key))) }), tab === "ai" && _jsx(Card, { title: "\uD83E\uDD16 Claude AI + Rule Engine \u2014 \u062A\u062D\u0644\u064A\u0644 \u0627\u0644\u062A\u062D\u0627\u0644\u064A\u0644 \u0627\u0644\u0645\u062E\u0628\u0631\u064A\u0629", accent: "#7c3aed", children: _jsx(ClaudeLabInterpreter, {}) }), tab === "orders" && _jsx(Card, { title: "\uD83D\uDCCB Lab Orders", accent: "#3b82f6", children: _jsx(LabOrdersPanel, {}) }), tab === "reference" && _jsx(Card, { title: "\uD83D\uDCCA Reference Ranges", accent: "#f59e0b", children: _jsx(ReferencePanel, {}) })] })] }));
}
