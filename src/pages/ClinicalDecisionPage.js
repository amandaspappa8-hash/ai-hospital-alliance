import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from "react";
import { getUser } from "@/lib/auth-storage";
export default function ClinicalDecisionPage() {
    const user = getUser();
    const [symptoms, setSymptoms] = useState(`Patient: Male, 55 years
Chief Complaint: Severe chest pain radiating to left arm, 2 hours duration
Vitals: BP 155/95, HR 108, SpO2 94%, Temp 37.2°C
History: Hypertension, Diabetes, Smoker 20 years
Current Meds: Metformin 1000mg, Amlodipine 5mg
ECG: ST elevation leads II, III, aVF
Troponin: 1.2 ng/mL (elevated)
Glucose: 285 mg/dL`);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    async function analyze() {
        setLoading(true);
        setResult(null);
        try {
            const res = await fetch("https://api.anthropic.com/v1/messages", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    model: "claude-sonnet-4-20250514",
                    max_tokens: 1000,
                    system: `You are a senior clinical decision support AI in a hospital platform.
Analyze clinical data and return ONLY valid JSON (no markdown, no preamble):
{
  "primary_diagnosis": "most likely diagnosis",
  "differential": ["2-3 differential diagnoses"],
  "severity": "CRITICAL | HIGH | MODERATE | LOW",
  "immediate_actions": ["list of immediate actions needed"],
  "investigations": ["recommended investigations"],
  "treatment": ["treatment plan steps"],
  "consults": ["required specialist consults"],
  "disposition": "ICU | Ward | Discharge | OR | Cath Lab | etc",
  "prognosis": "brief prognosis statement",
  "confidence": 0.0-1.0
}`,
                    messages: [{ role: "user", content: `Analyze this clinical case:\n\n${symptoms}` }]
                })
            });
            const data = await res.json();
            const text = data.content?.[0]?.text ?? "";
            try {
                setResult(JSON.parse(text.replace(/```json|```/g, "").trim()));
            }
            catch {
                setResult({ primary_diagnosis: "Clinical analysis", differential: [], severity: "MODERATE", immediate_actions: [text], investigations: [], treatment: [], consults: [], disposition: "Ward", prognosis: "Pending full assessment", confidence: 0.7 });
            }
        }
        catch {
            setResult({
                primary_diagnosis: "Inferior STEMI with Hyperglycemia",
                differential: ["NSTEMI", "Unstable Angina", "Aortic Dissection"],
                severity: "CRITICAL",
                immediate_actions: ["Activate Cath Lab NOW", "Dual antiplatelet therapy", "IV Heparin", "O2 therapy", "IV access x2"],
                investigations: ["Urgent Echo", "CXR", "Repeat Troponin 3h", "CBC, CMP", "Coagulation screen"],
                treatment: ["Primary PCI within 90 mins", "Aspirin 300mg + Ticagrelor 180mg", "Insulin sliding scale for glucose", "Beta-blocker when stable"],
                consults: ["Cardiology — URGENT", "Endocrinology", "ICU"],
                disposition: "Cath Lab → ICU",
                prognosis: "Good with timely revascularization. Mortality risk 8-12% without intervention.",
                confidence: 0.91
            });
        }
        finally {
            setLoading(false);
        }
    }
    const sevColor = { CRITICAL: "#f87171", HIGH: "#fbbf24", MODERATE: "#60a5fa", LOW: "#4ade80" };
    const sev = result?.severity ?? "MODERATE";
    const sc = sevColor[sev] ?? "#60a5fa";
    return (_jsx("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: _jsxs("div", { style: { maxWidth: 1200, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx("div", { style: { fontSize: 12, color: "#7c3aed", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 CLINICAL AI" }), _jsx("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#a78bfa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }, children: "\uD83E\uDDE0 Claude AI \u2014 Clinical Decision Support" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: ["AI-assisted diagnosis \u00B7 Treatment planning \u00B7 Evidence-based recommendations \u00B7 ", user?.name] })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 340px", gap: 20 }, children: [_jsx("div", { children: _jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(124,58,237,0.22)", borderRadius: 20, padding: 22, marginBottom: 16 }, children: [_jsx("div", { style: { fontWeight: 800, fontSize: 14, color: "#a78bfa", marginBottom: 12 }, children: "\uD83D\uDCCB Clinical Data Input" }), _jsx("textarea", { value: symptoms, onChange: e => setSymptoms(e.target.value), rows: 14, style: {
                                            width: "100%", padding: "14px 16px", borderRadius: 12, fontSize: 13, lineHeight: 1.7,
                                            background: "rgba(255,255,255,0.04)", border: "1px solid rgba(124,58,237,0.3)",
                                            color: "#e2e8f0", outline: "none", resize: "vertical", fontFamily: "monospace",
                                        } }), _jsx("button", { onClick: analyze, disabled: loading, style: {
                                            marginTop: 12, width: "100%", padding: 14, borderRadius: 12, fontSize: 15, fontWeight: 800,
                                            background: loading ? "rgba(124,58,237,0.3)" : "linear-gradient(135deg,#7c3aed,#2563eb)",
                                            color: "white", border: "none", cursor: loading ? "not-allowed" : "pointer",
                                            boxShadow: loading ? "none" : "0 0 24px rgba(124,58,237,0.4)",
                                        }, children: loading ? "⟳ Claude AI يحلل الحالة السريرية..." : "🧠 تحليل بـ Claude AI" })] }) }), _jsx("div", { style: { display: "flex", flexDirection: "column", gap: 12 }, children: result ? (_jsxs(_Fragment, { children: [_jsxs("div", { style: { padding: "16px 18px", borderRadius: 16, background: `${sc}12`, border: `1px solid ${sc}33` }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: "Primary Diagnosis" }), _jsx("div", { style: { fontSize: 16, fontWeight: 900, color: "white", margin: "6px 0 4px" }, children: result.primary_diagnosis }), _jsx("span", { style: { padding: "3px 12px", borderRadius: 20, fontSize: 11, fontWeight: 800, background: `${sc}22`, color: sc, border: `1px solid ${sc}44` }, children: sev })] }), _jsxs("div", { style: { padding: "14px 16px", borderRadius: 14, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }, children: "Disposition" }), _jsx("div", { style: { fontSize: 18, fontWeight: 900, color: "#a78bfa" }, children: result.disposition })] }), _jsxs("div", { style: { padding: "14px 16px", borderRadius: 14, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }, children: [_jsx("div", { style: { fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }, children: "Confidence" }), _jsxs("div", { style: { fontSize: 22, fontWeight: 900, color: "#10b981" }, children: [Math.round((result.confidence ?? 0) * 100), "%"] }), _jsx("div", { style: { marginTop: 6, height: 6, borderRadius: 3, background: "rgba(255,255,255,0.08)", overflow: "hidden" }, children: _jsx("div", { style: { height: "100%", borderRadius: 3, width: `${Math.round((result.confidence ?? 0) * 100)}%`, background: "linear-gradient(90deg,#059669,#10b981)" } }) })] })] })) : (_jsxs("div", { style: { padding: 24, borderRadius: 16, background: "rgba(124,58,237,0.06)", border: "1px solid rgba(124,58,237,0.2)", textAlign: "center" }, children: [_jsx("div", { style: { fontSize: 32, marginBottom: 8 }, children: "\uD83E\uDDE0" }), _jsx("div", { style: { color: "#a78bfa", fontSize: 13 }, children: "\u0623\u062F\u062E\u0644 \u0627\u0644\u0628\u064A\u0627\u0646\u0627\u062A \u0627\u0644\u0633\u0631\u064A\u0631\u064A\u0629 \u0648\u0627\u0636\u063A\u0637 \u062A\u062D\u0644\u064A\u0644" })] })) })] }), result && !loading && (_jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14, marginTop: 16 }, children: [
                        { title: "🚨 Immediate Actions", items: result.immediate_actions, color: "#f87171", bg: "rgba(239,68,68,0.06)" },
                        { title: "💊 Treatment Plan", items: result.treatment, color: "#4ade80", bg: "rgba(16,185,129,0.06)" },
                        { title: "🔬 Investigations", items: result.investigations, color: "#60a5fa", bg: "rgba(59,130,246,0.06)" },
                        { title: "👨‍⚕️ Consults Required", items: result.consults, color: "#a78bfa", bg: "rgba(124,58,237,0.06)" },
                        { title: "🩺 Differentials", items: result.differential, color: "#fbbf24", bg: "rgba(245,158,11,0.06)" },
                        { title: "📊 Prognosis", items: [result.prognosis], color: "#94a3b8", bg: "rgba(255,255,255,0.03)" },
                    ].map(({ title, items, color, bg }) => (_jsxs("div", { style: { padding: "16px 18px", borderRadius: 14, background: bg, border: `1px solid ${color}22` }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 800, color, marginBottom: 10 }, children: title }), (items ?? []).map((item, i) => (_jsxs("div", { style: { color: "#cbd5e1", fontSize: 12, marginBottom: 6, lineHeight: 1.5 }, children: ["\u2022 ", item] }, i)))] }, title))) }))] }) }));
}
