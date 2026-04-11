import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import "../styles/medical-ui.css";
import { apiGet, apiPost } from "@/lib/api";
import VisitTimelineCard from "@/components/clinical/VisitTimelineCard";
import SmartOrdersCard from "@/components/clinical/SmartOrdersCard";
import DigitalSignatureCard from "@/components/clinical/DigitalSignatureCard";
import DecisionEngineCard from "@/components/clinical/DecisionEngineCard";
import { buildVisitTimeline } from "@/lib/visitTimeline";
import { buildSmartOrders } from "@/lib/smartOrders";
import { buildDigitalSignature } from "@/lib/digitalSignature";
import { runSmartDecisionEngine } from "@/lib/smartDecisionEngine";
export default function ClinicalDecisionPage() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const patientIdFromUrl = searchParams.get("patientId") ?? "";
    const complaintFromUrl = searchParams.get("complaint") ?? "";
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl);
    const [text, setText] = useState(complaintFromUrl || "chest pain, sweating, shortness of breath");
    const [hr, setHr] = useState("118");
    const [sbp, setSbp] = useState("95");
    const [temp, setTemp] = useState("38.6");
    const [spo2, setSpo2] = useState("91");
    const [notes, setNotes] = useState([]);
    const [error, setError] = useState("");
    const [sendingToNotes, setSendingToNotes] = useState(false);
    const [aiSummary, setAiSummary] = useState("");
    useEffect(() => {
        apiGet("/patients")
            .then((data) => {
            const rows = Array.isArray(data) ? data : [];
            setPatients(rows);
            if (!patientIdFromUrl && rows.length > 0) {
                setSelectedPatientId(rows[0].id);
            }
        })
            .catch(() => {
            setPatients([]);
            setError("Failed to load patients");
        });
    }, [patientIdFromUrl]);
    const selectedPatient = useMemo(() => {
        return patients.find((p) => String(p.id) === String(selectedPatientId)) || null;
    }, [patients, selectedPatientId]);
    useEffect(() => {
        if (!selectedPatient?.id)
            return;
        apiGet(`/notes/${selectedPatient.id}`)
            .then((data) => setNotes(Array.isArray(data) ? data : []))
            .catch(() => setNotes([]));
    }, [selectedPatient?.id]);
    const result = useMemo(() => {
        return {
            impression: "Primary concern: Acute Coronary Syndrome. Severity is RED with estimated risk score 90/100.",
            recommendedPlan: "Recommended routing: Cardiology, Internal Medicine. Suggested labs: Troponin, CK-MB, CBC, CRP, ABG. Suggested medications: Aspirin, Paracetamol.",
            nextStepSummary: "Immediate next steps: Supplemental Oxygen, ICU consideration, immediate emergency management, continuous monitoring.",
        };
    }, []);
    const timelineItems = buildVisitTimeline(selectedPatient);
    const smartOrders = buildSmartOrders(selectedPatient);
    const digitalSignature = buildDigitalSignature("Dr Mohammed Elfallah");
    const decisionResult = runSmartDecisionEngine(selectedPatient);
    const generateClinicalSummary = () => {
        const summary = "Clinical Impression:\nCardiac risk suspected\n\n" +
            "Recommended Plan:\nECG + Troponin\n\n" +
            "Next Step:\nAdmit patient";
        setAiSummary(summary);
    };
    async function sendSummaryToNotes() {
        if (!selectedPatient?.id)
            return;
        if (!aiSummary.trim())
            return;
        setSendingToNotes(true);
        try {
            await apiPost(`/notes/${selectedPatient.id}`, { text: aiSummary });
            const data = await apiGet(`/notes/${selectedPatient.id}`);
            setNotes(Array.isArray(data) ? data : []);
        }
        finally {
            setSendingToNotes(false);
        }
    }
    return (_jsxs("div", { style: { padding: 24, color: "white" }, children: [_jsx("h1", { className: "page-title", children: "AI Clinical Decision Support" }), error && (_jsx("div", { style: { color: "#fca5a5", marginBottom: 16 }, children: error })), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "2fr 1fr", gap: 18 }, children: [_jsxs("div", { className: "med-card", style: { padding: 18 }, children: [_jsx("div", { style: { marginBottom: 12, fontWeight: 700 }, children: "Patient Context" }), _jsxs("select", { value: selectedPatientId, onChange: (e) => setSelectedPatientId(e.target.value), style: inputStyle, children: [_jsx("option", { value: "", children: "Select patient" }), patients.map((p) => (_jsxs("option", { value: p.id, children: [p.name, " (", p.id, ")"] }, p.id)))] }), _jsx("div", { style: { marginTop: 16, marginBottom: 8, fontWeight: 700 }, children: "Clinical Complaint Input" }), _jsx("textarea", { value: text, onChange: (e) => setText(e.target.value), style: textareaStyle }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }, children: [_jsx("input", { value: hr, onChange: (e) => setHr(e.target.value), style: inputStyle, placeholder: "HR" }), _jsx("input", { value: sbp, onChange: (e) => setSbp(e.target.value), style: inputStyle, placeholder: "SBP" }), _jsx("input", { value: temp, onChange: (e) => setTemp(e.target.value), style: inputStyle, placeholder: "Temp" }), _jsx("input", { value: spo2, onChange: (e) => setSpo2(e.target.value), style: inputStyle, placeholder: "SpO2" })] }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap", marginTop: 16 }, children: [_jsx("button", { onClick: generateClinicalSummary, style: buttonBlue, children: "Generate Clinical Summary" }), _jsx("button", { onClick: sendSummaryToNotes, style: buttonGreen, children: sendingToNotes ? "Sending..." : "Send Summary to Notes" }), _jsx("button", { onClick: () => navigate(`/reports?patientId=${selectedPatient?.id ?? ""}`), style: buttonPink, children: "Send Summary to Reports" })] }), selectedPatient && (_jsxs("div", { style: { marginTop: 18, padding: 14, border: "1px solid #374151", borderRadius: 10 }, children: [_jsx("div", { style: { fontWeight: 700 }, children: selectedPatient.name }), _jsxs("div", { style: { opacity: 0.75, marginTop: 6 }, children: ["Department: ", selectedPatient.department ?? "N/A"] }), _jsxs("div", { style: { opacity: 0.75, marginTop: 6 }, children: ["Condition: ", selectedPatient.condition ?? "N/A"] })] })), _jsxs("div", { style: { display: "grid", gap: 18, marginTop: 18, marginBottom: 18, border: "2px solid #38bdf8", padding: 12, borderRadius: 12 }, children: [_jsx(VisitTimelineCard, { items: timelineItems }), _jsx(SmartOrdersCard, { orders: smartOrders }), _jsx(DecisionEngineCard, { result: decisionResult }), _jsx(DigitalSignatureCard, { signature: digitalSignature })] }), aiSummary && (_jsxs("div", { className: "med-card", style: { marginTop: 18, padding: 16 }, children: [_jsx("h3", { children: "AI Clinical Summary" }), _jsx("pre", { style: { whiteSpace: "pre-wrap" }, children: aiSummary })] })), _jsxs("div", { className: "med-card", style: { marginTop: 18, padding: 16 }, children: [_jsx("h3", { children: "Patient Notes" }), notes.length === 0 ? (_jsx("div", { style: { opacity: 0.75 }, children: "No notes for this patient." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: notes.map((note) => (_jsx("div", { style: { border: "1px solid #374151", borderRadius: 10, padding: 12 }, children: note.text }, note.id))) }))] })] }), _jsxs("div", { style: { display: "grid", gap: 18 }, children: [_jsxs("div", { className: "med-card", style: { padding: 16 }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 700, marginBottom: 12 }, children: "Clinical Impression" }), _jsx("div", { style: summaryTextStyle, children: result.impression })] }), _jsxs("div", { className: "med-card", style: { padding: 16 }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 700, marginBottom: 12 }, children: "Recommended Plan" }), _jsx("div", { style: summaryTextStyle, children: result.recommendedPlan })] }), _jsxs("div", { className: "med-card", style: { padding: 16 }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 700, marginBottom: 12 }, children: "Next Step Summary" }), _jsx("div", { style: summaryTextStyle, children: result.nextStepSummary })] })] })] })] }));
}
const inputStyle = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 10,
    border: "1px solid #334155",
    background: "#020617",
    color: "white",
};
const textareaStyle = {
    width: "100%",
    minHeight: 140,
    padding: "12px",
    borderRadius: 10,
    border: "1px solid #334155",
    background: "#020617",
    color: "white",
};
const summaryTextStyle = {
    lineHeight: 1.7,
    opacity: 0.95,
};
const buttonBlue = {
    padding: "12px 16px",
    borderRadius: 10,
    border: "1px solid #38bdf8",
    background: "#0284c7",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
const buttonGreen = {
    padding: "12px 16px",
    borderRadius: 10,
    border: "1px solid #22c55e",
    background: "#166534",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
const buttonPink = {
    padding: "12px 16px",
    borderRadius: 10,
    border: "1px solid #f472b6",
    background: "#be185d",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
