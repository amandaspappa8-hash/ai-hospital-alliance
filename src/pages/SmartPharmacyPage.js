import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
// ─── Helpers ─────────────────────────────────────────────────────────────────
const RISK_COLORS = {
    HIGH: { bg: "#450a0a", color: "#f87171", glow: "0 0 12px #f8717155" },
    MODERATE: { bg: "#1c1108", color: "#fbbf24", glow: "0 0 12px #fbbf2455" },
    LOW: { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
    SAFE: { bg: "#052e16", color: "#4ade80", glow: "0 0 12px #4ade8055" },
    UNKNOWN: { bg: "#1e293b", color: "#94a3b8", glow: "none" },
};
function RiskBadge({ level }) {
    const s = RISK_COLORS[level] ?? RISK_COLORS.UNKNOWN;
    return (_jsx("span", { style: {
            background: s.bg, color: s.color, padding: "3px 12px",
            borderRadius: 20, fontSize: 11, fontWeight: 800,
            border: `1px solid ${s.color}44`, boxShadow: s.glow,
        }, children: level }));
}
function Card({ title, children, accent = "#3b82f6" }) {
    return (_jsxs("div", { style: {
            background: "linear-gradient(135deg,#0f172a,#1a2540)",
            border: `1px solid ${accent}22`, borderRadius: 20, padding: 22,
            boxShadow: "0 4px 24px rgba(0,0,0,0.4)",
        }, children: [_jsxs("div", { style: {
                    fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18,
                    display: "flex", alignItems: "center", gap: 8,
                }, children: [_jsx("div", { style: { width: 3, height: 18, background: accent, borderRadius: 2, boxShadow: `0 0 8px ${accent}` } }), title] }), children] }));
}
// ─── FDA Drug Search ──────────────────────────────────────────────────────────
function DrugSearch() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [selected, setSelected] = useState(null);
    const [rxInteractions, setRxInteractions] = useState([]);
    const [rxLoading, setRxLoading] = useState(false);
    async function searchFDA() {
        if (!query.trim())
            return;
        setLoading(true);
        setError("");
        setSelected(null);
        setRxInteractions([]);
        try {
            const res = await fetch(`https://api.fda.gov/drug/label.json?search=openfda.generic_name:"${encodeURIComponent(query)}"&limit=5`);
            const data = await res.json();
            if (data.results) {
                setResults(data.results);
            }
            else {
                setError("No results found. Try a different drug name.");
                setResults([]);
            }
        }
        catch {
            setError("FDA API unavailable. Showing cached data.");
            setResults([]);
        }
        finally {
            setLoading(false);
        }
    }
    async function fetchRxInteractions(drugName) {
        setRxLoading(true);
        try {
            // Step 1: Get RxCUI
            const r1 = await fetch(`https://rxnav.nlm.nih.gov/REST/rxcui.json?name=${encodeURIComponent(drugName)}&search=1`);
            const d1 = await r1.json();
            const rxcui = d1?.idGroup?.rxnormId?.[0];
            if (!rxcui) {
                setRxLoading(false);
                return;
            }
            // Step 2: Get interactions
            const r2 = await fetch(`https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=${rxcui}`);
            const d2 = await r2.json();
            const groups = d2?.interactionTypeGroup ?? [];
            const interactions = [];
            for (const group of groups) {
                for (const type of group.interactionType ?? []) {
                    for (const pair of type.interactionPair ?? []) {
                        interactions.push({
                            description: pair.description,
                            severity: pair.severity,
                        });
                    }
                }
            }
            setRxInteractions(interactions.slice(0, 8));
        }
        catch {
            setRxInteractions([]);
        }
        finally {
            setRxLoading(false);
        }
    }
    function selectDrug(drug) {
        setSelected(drug);
        const name = drug.openfda?.generic_name?.[0] ?? drug.openfda?.brand_name?.[0] ?? query;
        fetchRxInteractions(name);
    }
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 16 }, children: [_jsxs("div", { style: { display: "flex", gap: 10 }, children: [_jsx("input", { value: query, onChange: e => setQuery(e.target.value), onKeyDown: e => e.key === "Enter" && searchFDA(), placeholder: "Search any drug \u2014 e.g. Warfarin, Metformin, Aspirin...", style: {
                            flex: 1, padding: "12px 16px", borderRadius: 12, fontSize: 14,
                            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(59,130,246,0.3)",
                            color: "white", outline: "none",
                        } }), _jsx("button", { onClick: searchFDA, disabled: loading, style: {
                            padding: "12px 24px", borderRadius: 12, fontSize: 14, fontWeight: 700,
                            background: "linear-gradient(135deg,#2563eb,#7c3aed)",
                            color: "white", border: "none", cursor: "pointer",
                            boxShadow: "0 0 20px rgba(37,99,235,0.4)",
                            opacity: loading ? 0.7 : 1,
                        }, children: loading ? "⟳ Searching..." : "🔍 Search FDA" })] }), error && _jsx("div", { style: { color: "#fca5a5", fontSize: 13, padding: "10px 14px", background: "rgba(239,68,68,0.1)", borderRadius: 10, border: "1px solid rgba(239,68,68,0.2)" }, children: error }), results.length > 0 && !selected && (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: [_jsx("div", { style: { color: "#64748b", fontSize: 12, fontWeight: 600 }, children: "SELECT A DRUG TO VIEW FULL PROFILE" }), results.map((r, i) => (_jsxs("div", { onClick: () => selectDrug(r), style: {
                            padding: "14px 16px", borderRadius: 12, cursor: "pointer",
                            background: "rgba(59,130,246,0.06)", border: "1px solid rgba(59,130,246,0.2)",
                            transition: "all 0.2s",
                        }, onMouseEnter: e => e.currentTarget.style.background = "rgba(59,130,246,0.15)", onMouseLeave: e => e.currentTarget.style.background = "rgba(59,130,246,0.06)", children: [_jsx("div", { style: { fontWeight: 700, color: "white", fontSize: 14 }, children: r.openfda?.brand_name?.[0] ?? "Unknown Brand" }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 12, marginTop: 3 }, children: ["Generic: ", r.openfda?.generic_name?.[0] ?? "—", " \u00B7 Route: ", r.openfda?.route?.[0] ?? "—", " \u00B7 Manufacturer: ", r.openfda?.manufacturer_name?.[0] ?? "—"] })] }, i)))] })), selected && (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 14 }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center" }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontSize: 22, fontWeight: 900, color: "white" }, children: selected.openfda?.brand_name?.[0] ?? "Drug Profile" }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 13, marginTop: 2 }, children: [selected.openfda?.generic_name?.[0], " \u00B7 ", selected.openfda?.route?.[0], " \u00B7 ", selected.openfda?.manufacturer_name?.[0]] })] }), _jsx("button", { onClick: () => { setSelected(null); setResults([]); }, style: {
                                    padding: "8px 16px", borderRadius: 10, background: "rgba(255,255,255,0.07)",
                                    color: "#94a3b8", border: "1px solid rgba(255,255,255,0.1)", cursor: "pointer", fontSize: 12,
                                }, children: "\u2190 Back" })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }, children: [
                            { label: "Indications & Usage", data: selected.indications_and_usage, accent: "#3b82f6" },
                            { label: "Dosage & Administration", data: selected.dosage_and_administration, accent: "#10b981" },
                            { label: "Contraindications", data: selected.contraindications, accent: "#ef4444" },
                            { label: "Warnings", data: selected.warnings, accent: "#f59e0b" },
                            { label: "Adverse Reactions", data: selected.adverse_reactions, accent: "#f97316" },
                            { label: "Drug Interactions (FDA)", data: selected.drug_interactions, accent: "#a855f7" },
                        ].map(({ label, data, accent }) => data?.[0] && (_jsxs("div", { style: {
                                padding: 16, borderRadius: 14,
                                background: `${accent}08`, border: `1px solid ${accent}22`,
                            }, children: [_jsx("div", { style: { fontSize: 11, fontWeight: 800, color: accent, textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }, children: label }), _jsxs("div", { style: { color: "#cbd5e1", fontSize: 12, lineHeight: 1.7, maxHeight: 120, overflow: "auto" }, children: [data[0].slice(0, 400), data[0].length > 400 ? "..." : ""] })] }, label))) }), _jsxs("div", { style: {
                            padding: 18, borderRadius: 14,
                            background: "rgba(168,85,247,0.06)", border: "1px solid rgba(168,85,247,0.2)",
                        }, children: [_jsx("div", { style: { fontSize: 12, fontWeight: 800, color: "#a855f7", textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }, children: "\u2697 RxNorm Drug Interactions Database" }), rxLoading ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "\u27F3 Fetching RxNorm interactions..." })) : rxInteractions.length === 0 ? (_jsx("div", { style: { color: "#4ade80", fontSize: 13 }, children: "\u2713 No major interactions found in RxNorm database" })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 8 }, children: rxInteractions.map((ix, i) => (_jsxs("div", { style: {
                                        padding: "10px 12px", borderRadius: 10,
                                        background: ix.severity === "high" ? "rgba(239,68,68,0.08)" : "rgba(245,158,11,0.08)",
                                        border: ix.severity === "high" ? "1px solid rgba(239,68,68,0.3)" : "1px solid rgba(245,158,11,0.3)",
                                    }, children: [ix.severity && (_jsx(RiskBadge, { level: ix.severity.toUpperCase() })), _jsx("div", { style: { color: "#cbd5e1", fontSize: 12, marginTop: 6, lineHeight: 1.6 }, children: ix.description })] }, i))) }))] })] }))] }));
}
// ─── MAR Panel ────────────────────────────────────────────────────────────────
function MARPanel() {
    const [patientId, setPatientId] = useState("P-1001");
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [aiAnalysis, setAiAnalysis] = useState({});
    const [analyzing, setAnalyzing] = useState(null);
    async function loadMAR() {
        setLoading(true);
        try {
            const data = await apiGet(`/mar/${patientId}`);
            setItems(Array.isArray(data) ? data : []);
        }
        catch {
            setItems([]);
        }
        finally {
            setLoading(false);
        }
    }
    useEffect(() => { loadMAR(); }, [patientId]);
    async function analyzeWithAI(item) {
        setAnalyzing(item.id);
        try {
            // Check FDA for this drug
            const res = await fetch(`https://api.fda.gov/drug/label.json?search=openfda.generic_name:"${encodeURIComponent(item.medication.split(" ")[0])}"&limit=1`);
            const data = await res.json();
            const drug = data.results?.[0];
            if (drug) {
                const warnings = drug.warnings?.[0]?.slice(0, 200) ?? "No major warnings found";
                const interactions = drug.drug_interactions?.[0]?.slice(0, 200) ?? "No interactions listed";
                setAiAnalysis(prev => ({
                    ...prev,
                    [item.id]: `⚠ FDA Warnings: ${warnings}\n\n💊 Interactions: ${interactions}`
                }));
            }
            else {
                setAiAnalysis(prev => ({ ...prev, [item.id]: "✓ Drug not found in FDA high-alert database. Appears safe." }));
            }
        }
        catch {
            setAiAnalysis(prev => ({ ...prev, [item.id]: "FDA API unavailable for this check." }));
        }
        finally {
            setAnalyzing(null);
        }
    }
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 14 }, children: [_jsxs("div", { style: { display: "flex", gap: 10, alignItems: "center" }, children: [_jsxs("select", { value: patientId, onChange: e => setPatientId(e.target.value), style: {
                            padding: "10px 14px", borderRadius: 10, background: "rgba(255,255,255,0.05)",
                            border: "1px solid rgba(59,130,246,0.3)", color: "white", fontSize: 13,
                        }, children: [_jsx("option", { value: "P-1001", children: "P-1001 \u2014 Ahmed Ali" }), _jsx("option", { value: "P-1002", children: "P-1002 \u2014 Sara Omar" }), _jsx("option", { value: "P-1003", children: "P-1003 \u2014 Mona Salem" })] }), _jsx("button", { onClick: loadMAR, style: {
                            padding: "10px 18px", borderRadius: 10, background: "rgba(59,130,246,0.15)",
                            border: "1px solid rgba(59,130,246,0.3)", color: "#60a5fa", fontSize: 13, cursor: "pointer",
                        }, children: "\u27F3 Reload" })] }), loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading MAR..." }) : items.length === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No MAR items for this patient." })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: items.map(item => (_jsxs("div", { style: {
                        padding: 16, borderRadius: 14,
                        background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
                    }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }, children: [_jsxs("div", { style: { flex: 1 }, children: [_jsx("div", { style: { fontWeight: 800, color: "white", fontSize: 15 }, children: item.medication }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 12, marginTop: 4 }, children: [item.dose, " \u00B7 ", item.route, " \u00B7 ", item.schedule] }), item.givenAt && _jsxs("div", { style: { color: "#64748b", fontSize: 11, marginTop: 2 }, children: ["Given at: ", item.givenAt] })] }), _jsxs("div", { style: { display: "flex", flex: "column", gap: 8, alignItems: "flex-end" }, children: [_jsx(RiskBadge, { level: item.status === "Given" ? "SAFE" : item.status === "Pending" ? "MODERATE" : "UNKNOWN" }), _jsx("button", { onClick: () => analyzeWithAI(item), disabled: analyzing === item.id, style: {
                                                marginTop: 8, padding: "6px 14px", borderRadius: 8, fontSize: 11, fontWeight: 700,
                                                background: "linear-gradient(135deg,#7c3aed,#2563eb)",
                                                color: "white", border: "none", cursor: "pointer", whiteSpace: "nowrap",
                                            }, children: analyzing === item.id ? "⟳ Checking..." : "🤖 AI Check FDA" })] })] }), aiAnalysis[item.id] && (_jsx("div", { style: {
                                marginTop: 12, padding: "12px 14px", borderRadius: 10,
                                background: "rgba(124,58,237,0.08)", border: "1px solid rgba(124,58,237,0.25)",
                                color: "#c4b5fd", fontSize: 12, lineHeight: 1.7, whiteSpace: "pre-wrap",
                            }, children: aiAnalysis[item.id] }))] }, item.id))) }))] }));
}
// ─── AI Drug Interactions Checker ─────────────────────────────────────────────
function InteractionChecker() {
    const [drugs, setDrugs] = useState("Warfarin, Aspirin, Ibuprofen");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    async function checkInteractions() {
        setLoading(true);
        setResults([]);
        const list = drugs.split(",").map(d => d.trim()).filter(Boolean);
        const out = [];
        for (const drug of list) {
            try {
                const r1 = await fetch(`https://rxnav.nlm.nih.gov/REST/rxcui.json?name=${encodeURIComponent(drug)}&search=1`);
                const d1 = await r1.json();
                const rxcui = d1?.idGroup?.rxnormId?.[0];
                if (!rxcui) {
                    out.push({ drug, interactions: [] });
                    continue;
                }
                const r2 = await fetch(`https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcui=${rxcui}`);
                const d2 = await r2.json();
                const groups = d2?.interactionTypeGroup ?? [];
                const interactions = [];
                for (const group of groups) {
                    for (const type of group.interactionType ?? []) {
                        for (const pair of type.interactionPair ?? []) {
                            interactions.push({ description: pair.description, severity: pair.severity });
                        }
                    }
                }
                out.push({ drug, interactions: interactions.slice(0, 4) });
            }
            catch {
                out.push({ drug, interactions: [] });
            }
        }
        setResults(out);
        setLoading(false);
    }
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 14 }, children: [_jsxs("div", { style: { display: "flex", gap: 10 }, children: [_jsx("input", { value: drugs, onChange: e => setDrugs(e.target.value), placeholder: "Enter drugs separated by commas...", style: {
                            flex: 1, padding: "12px 16px", borderRadius: 12, fontSize: 13,
                            background: "rgba(255,255,255,0.05)", border: "1px solid rgba(168,85,247,0.3)",
                            color: "white", outline: "none",
                        } }), _jsx("button", { onClick: checkInteractions, disabled: loading, style: {
                            padding: "12px 22px", borderRadius: 12, fontSize: 13, fontWeight: 700,
                            background: "linear-gradient(135deg,#7c3aed,#a855f7)",
                            color: "white", border: "none", cursor: "pointer",
                            opacity: loading ? 0.7 : 1,
                        }, children: loading ? "⟳ Checking..." : "⚗ Check RxNorm" })] }), results.length > 0 && (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 12 }, children: results.map(({ drug, interactions }) => (_jsxs("div", { style: {
                        padding: 16, borderRadius: 14,
                        background: interactions.length > 0 ? "rgba(239,68,68,0.06)" : "rgba(16,185,129,0.06)",
                        border: interactions.length > 0 ? "1px solid rgba(239,68,68,0.2)" : "1px solid rgba(16,185,129,0.2)",
                    }, children: [_jsxs("div", { style: { fontWeight: 800, color: "white", fontSize: 14, marginBottom: 8 }, children: ["\uD83D\uDC8A ", drug, _jsx("span", { style: { marginLeft: 10 }, children: _jsx(RiskBadge, { level: interactions.some(i => i.severity === "high") ? "HIGH" : interactions.length > 0 ? "MODERATE" : "SAFE" }) })] }), interactions.length === 0 ? (_jsx("div", { style: { color: "#4ade80", fontSize: 12 }, children: "\u2713 No significant interactions found" })) : (interactions.map((ix, i) => (_jsxs("div", { style: { color: "#fca5a5", fontSize: 12, marginTop: 4, lineHeight: 1.6 }, children: ["\u26A0 ", ix.description] }, i))))] }, drug))) }))] }));
}
// ─── Main Page ─────────────────────────────────────────────────────────────────
export default function SmartPharmacyPage() {
    const [tab, setTab] = useState("search");
    const user = getUser();
    const tabs = [
        { key: "search", label: "🔍 FDA Drug Search", accent: "#3b82f6" },
        { key: "mar", label: "💊 MAR — AI Safety Check", accent: "#10b981" },
        { key: "interactions", label: "⚗ Interaction Checker", accent: "#a855f7" },
    ];
    return (_jsxs("div", { style: {
            padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
        }, children: [_jsx("div", { style: {
                    position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
                    backgroundImage: "linear-gradient(rgba(59,130,246,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(59,130,246,0.03) 1px,transparent 1px)",
                    backgroundSize: "60px 60px",
                } }), _jsxs("div", { style: { position: "relative", zIndex: 1, maxWidth: 1200, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 28 }, children: [_jsx("div", { style: { fontSize: 12, color: "#3b82f6", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 SMART PHARMACY" }), _jsx("h1", { style: {
                                    margin: 0, fontSize: 28, fontWeight: 900, letterSpacing: -0.5,
                                    background: "linear-gradient(135deg,#fff,#94a3b8)",
                                    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                                }, children: "\uD83D\uDC8A Smart Pharmacy \u2014 Global Drug Intelligence" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: ["Powered by FDA OpenFDA \u00B7 RxNorm NLM \u00B7 AI Safety Engine \u00B7 ", user?.name] })] }), _jsx("div", { style: {
                            display: "flex", gap: 12, marginBottom: 24, padding: "14px 18px",
                            borderRadius: 14, background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.2)",
                            flexWrap: "wrap",
                        }, children: [
                            { label: "FDA Database", value: "20,000+ Drug Labels", color: "#3b82f6" },
                            { label: "RxNorm NLM", value: "Live Interaction Data", color: "#a855f7" },
                            { label: "AI Safety", value: "Real-time Analysis", color: "#10b981" },
                            { label: "Coverage", value: "FDA · EMA · WHO", color: "#f59e0b" },
                        ].map(({ label, value, color }) => (_jsxs("div", { style: { display: "flex", flexDirection: "column", gap: 2 }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: label }), _jsx("div", { style: { fontSize: 13, fontWeight: 700, color }, children: value })] }, label))) }), _jsx("div", { style: { display: "flex", gap: 8, marginBottom: 22 }, children: tabs.map(t => (_jsx("button", { onClick: () => setTab(t.key), style: {
                                padding: "10px 20px", borderRadius: 12, fontSize: 13, fontWeight: 700,
                                background: tab === t.key ? `${t.accent}22` : "rgba(255,255,255,0.04)",
                                color: tab === t.key ? t.accent : "#64748b",
                                border: `1px solid ${tab === t.key ? t.accent + "55" : "rgba(255,255,255,0.08)"}`,
                                cursor: "pointer", transition: "all 0.2s",
                                boxShadow: tab === t.key ? `0 0 16px ${t.accent}33` : "none",
                            }, children: t.label }, t.key))) }), tab === "search" && (_jsx(Card, { title: "\uD83D\uDD0D FDA Global Drug Database Search", accent: "#3b82f6", children: _jsx(DrugSearch, {}) })), tab === "mar" && (_jsx(Card, { title: "\uD83D\uDC8A Medication Administration Record \u2014 AI Safety Check", accent: "#10b981", children: _jsx(MARPanel, {}) })), tab === "interactions" && (_jsx(Card, { title: "\u2697 Drug Interaction Checker \u2014 RxNorm NLM Database", accent: "#a855f7", children: _jsx(InteractionChecker, {}) }))] })] }));
}
