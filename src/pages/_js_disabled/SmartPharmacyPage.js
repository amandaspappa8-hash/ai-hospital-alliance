import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiDelete, apiGet, apiPost, apiPut } from "@/lib/api";
export default function SmartPharmacyPage() {
    const [searchParams] = useSearchParams();
    const patientId = searchParams.get("patientId") ?? "P-1001";
    const [items, setItems] = useState([]);
    const [medication, setMedication] = useState("");
    const [dose, setDose] = useState("");
    const [route, setRoute] = useState("");
    const [schedule, setSchedule] = useState("");
    const [search, setSearch] = useState("");
    const [intel, setIntel] = useState(null);
    const [intelError, setIntelError] = useState("");
    const [interactionData, setInteractionData] = useState(null);
    const [interactionError, setInteractionError] = useState("");
    const [doseSafety, setDoseSafety] = useState(null);
    const [doseSafetyError, setDoseSafetyError] = useState("");
    const [recommendations, setRecommendations] = useState(null);
    const [recommendationError, setRecommendationError] = useState("");
    const [patientAge, setPatientAge] = useState("45");
    const [reconciliation, setReconciliation] = useState(null);
    const [reconciliationError, setReconciliationError] = useState("");
    const [noteText, setNoteText] = useState("");
    const [selectedItemId, setSelectedItemId] = useState(null);
    const totalHighRisk = (interactionData?.summary.high_risk_count || 0) +
        (doseSafety?.summary.high_risk_count || 0);
    const totalModerateRisk = (interactionData?.summary.moderate_risk_count || 0) +
        (doseSafety?.summary.moderate_risk_count || 0);
    const hasCriticalRisk = totalHighRisk > 0;
    function load() {
        apiGet(`/mar/${patientId}`).then((data) => {
            setItems(data);
            loadInteractions();
            loadDoseSafety();
            loadRecommendations();
            loadReconciliation();
        });
    }
    function loadInteractions() {
        apiGet(`/drug-intel/interactions/${patientId}`)
            .then(setInteractionData)
            .catch((err) => {
            console.error(err);
            setInteractionError("Drug interaction analysis failed");
        });
    }
    function loadDoseSafety() {
        apiGet(`/drug-intel/dose-safety/${patientId}?age=${encodeURIComponent(patientAge || "45")}`)
            .then(setDoseSafety)
            .catch((err) => {
            console.error(err);
            setDoseSafetyError("Dose safety analysis failed");
        });
    }
    function loadRecommendations() {
        apiGet(`/drug-intel/recommendations/${patientId}?age=${encodeURIComponent(patientAge || "45")}`)
            .then(setRecommendations)
            .catch((err) => {
            console.error(err);
            setRecommendationError("Medication recommendation analysis failed");
        });
    }
    function loadReconciliation() {
        apiGet(`/drug-intel/reconciliation/${patientId}`)
            .then(setReconciliation)
            .catch((err) => {
            console.error(err);
            setReconciliationError("Medication reconciliation failed");
        });
    }
    useEffect(() => {
        load();
    }, [patientId]);
    function createItem() {
        apiPost(`/mar/${patientId}`, {
            medication,
            dose,
            route,
            schedule,
        }).then(() => {
            setMedication("");
            setDose("");
            setRoute("");
            setSchedule("");
            load();
        });
    }
    function give(id) {
        apiPut(`/mar/${patientId}/${id}/status`, {
            status: "Given",
            givenAt: new Date().toLocaleTimeString(),
        }).then(load);
    }
    function remove(id) {
        apiDelete(`/mar/${patientId}/${id}`).then(load);
    }
    function pharmacistReview(status) {
        if (!selectedItemId)
            return;
        apiPut(`/mar/${patientId}/${selectedItemId}/pharmacist-review`, {
            status,
            note: noteText,
        }).then(() => {
            setNoteText("");
            setSelectedItemId(null);
            load();
        });
    }
    function searchDrug() {
        if (!search.trim())
            return;
        setIntelError("");
        apiGet(`/drug-intel/search?q=${encodeURIComponent(search.trim())}`)
            .then(setIntel)
            .catch((err) => {
            console.error(err);
            setIntelError("Drug intelligence search failed");
        });
    }
    const rxConcepts = intel?.rxnorm?.drugGroup?.conceptGroup?.flatMap((group) => group.conceptProperties || []) || [];
    const fdaResult = intel?.openfda?.results?.[0] || null;
    const brandName = fdaResult?.openfda?.brand_name?.join(", ") || "-";
    const genericName = fdaResult?.openfda?.generic_name?.join(", ") || "-";
    const routeNames = fdaResult?.openfda?.route?.join(", ") || "-";
    const dosageForm = fdaResult?.openfda?.dosage_form?.join(", ") || "-";
    const manufacturer = fdaResult?.openfda?.manufacturer_name?.join(", ") || "-";
    const activeIngredient = fdaResult?.active_ingredient?.[0] || "-";
    const indications = fdaResult?.indications_and_usage?.[0] || "-";
    const dosageInfo = fdaResult?.dosage_and_administration?.[0] || "-";
    const warnings = fdaResult?.warnings?.[0] || "-";
    const doNotUse = fdaResult?.do_not_use?.[0] || "-";
    const askDoctor = fdaResult?.ask_doctor?.[0] || "-";
    const askPharmacist = fdaResult?.ask_doctor_or_pharmacist?.[0] || "-";
    const stopUse = fdaResult?.stop_use?.[0] || "-";
    return (_jsxs("div", { style: { padding: 30, color: "white", background: "#0b1220", minHeight: "100vh" }, children: [_jsx("h1", { style: { fontSize: 30, marginBottom: 20 }, children: "Smart Pharmacy" }), _jsxs("div", { style: {
                    border: hasCriticalRisk ? "1px solid #ef4444" : "1px solid #f59e0b",
                    background: hasCriticalRisk ? "rgba(127,29,29,0.35)" : "rgba(120,53,15,0.35)",
                    borderRadius: 16,
                    padding: 16,
                    marginBottom: 20,
                }, children: [_jsx("div", { style: { fontSize: 20, fontWeight: 800 }, children: "Clinical Pharmacy Risk Dashboard" }), _jsxs("div", { style: { marginTop: 10 }, children: ["High Risk Findings: ", _jsx("strong", { children: totalHighRisk })] }), _jsxs("div", { children: ["Moderate Risk Findings: ", _jsx("strong", { children: totalModerateRisk })] }), _jsx("div", { style: { marginTop: 12, color: "#facc15", fontWeight: 700 }, children: hasCriticalRisk
                            ? "Immediate pharmacist / physician review recommended."
                            : "No critical risk detected, but review is still recommended." })] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Pharmacist Action Center" }), _jsxs("div", { style: { display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }, children: [_jsxs("div", { style: badge, children: ["Patient ID: ", patientId] }), _jsx("input", { style: { ...input, maxWidth: 160 }, placeholder: "Patient age", value: patientAge, onChange: (e) => setPatientAge(e.target.value) }), _jsx("button", { style: button, onClick: () => {
                                            loadDoseSafety();
                                            loadRecommendations();
                                        }, children: "Refresh Clinical Review" })] }), _jsxs("div", { style: { marginTop: 16, display: "grid", gap: 10 }, children: [_jsxs("select", { value: selectedItemId ?? "", onChange: (e) => setSelectedItemId(e.target.value ? Number(e.target.value) : null), style: input, children: [_jsx("option", { value: "", children: "Select medication for pharmacist action" }), items.map((item) => (_jsxs("option", { value: item.id, children: [item.medication, " \u2014 ", item.status] }, item.id)))] }), _jsx("textarea", { style: { ...input, minHeight: 110, resize: "vertical" }, placeholder: "Pharmacist note", value: noteText, onChange: (e) => setNoteText(e.target.value) }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("button", { style: reviewButton, onClick: () => pharmacistReview("Reviewed"), children: "Review Medication Plan" }), _jsx("button", { style: holdButton, onClick: () => pharmacistReview("Held"), children: "Hold Medication" }), _jsx("button", { style: pharmacistButton, onClick: () => pharmacistReview("Needs Pharmacist Review"), children: "Needs Pharmacist Review" })] })] })] }), _jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Smart Medication Recommendation Layer" }), recommendationError ? _jsx("div", { style: { color: "#fca5a5", marginBottom: 12 }, children: recommendationError }) : null, recommendations ? (_jsxs("div", { style: { display: "grid", gap: 14 }, children: [_jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Recommendation Summary" }), _jsxs("div", { style: row, children: ["High priority: ", recommendations.summary.high_priority_count] }), _jsxs("div", { style: row, children: ["Moderate priority: ", recommendations.summary.moderate_priority_count] }), _jsxs("div", { style: row, children: ["Low priority: ", recommendations.summary.low_priority_count] })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Recommended Actions" }), recommendations.recommendations.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No recommendations available" })) : (recommendations.recommendations.map((item, idx) => (_jsxs("div", { style: {
                                                    ...row,
                                                    borderColor: item.priority === "high" ? "#ef4444" :
                                                        item.priority === "moderate" ? "#f59e0b" : "#243041",
                                                    background: item.priority === "high" ? "rgba(127,29,29,0.22)" :
                                                        item.priority === "moderate" ? "rgba(120,53,15,0.22)" : "#0f172a",
                                                }, children: [_jsx("div", { style: { fontWeight: 800 }, children: item.title }), _jsx("div", { style: { marginTop: 6 }, children: item.detail }), _jsxs("div", { style: { marginTop: 8, color: "#93c5fd" }, children: ["Suggested action: ", item.suggested_action] }), _jsxs("div", { style: { marginTop: 6, opacity: 0.8 }, children: ["Priority: ", item.priority, " \u2022 Type: ", item.type] })] }, idx))))] })] })) : (_jsx("div", { style: { opacity: 0.8 }, children: "Medication recommendations not loaded yet" }))] }), _jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Medication Reconciliation Layer" }), reconciliationError ? (_jsx("div", { style: { color: "#fca5a5", marginBottom: 12 }, children: reconciliationError })) : null, reconciliation ? (_jsxs("div", { style: { display: "grid", gap: 14 }, children: [_jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Reconciliation Summary" }), _jsxs("div", { style: row, children: ["High risk findings: ", reconciliation.summary.high_risk_count] }), _jsxs("div", { style: row, children: ["Moderate risk findings: ", reconciliation.summary.moderate_risk_count] }), _jsxs("div", { style: row, children: ["Has findings: ", reconciliation.summary.has_findings ? "Yes" : "No"] })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Home Medications" }), reconciliation.homeMeds.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No home medications" })) : (reconciliation.homeMeds.map((med, idx) => _jsx("div", { style: row, children: med }, idx)))] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Admission Medications" }), reconciliation.admissionMeds.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No admission medications" })) : (reconciliation.admissionMeds.map((med, idx) => _jsx("div", { style: row, children: med }, idx)))] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Discharge Medications" }), reconciliation.dischargeMeds.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No discharge medications" })) : (reconciliation.dischargeMeds.map((med, idx) => _jsx("div", { style: row, children: med }, idx)))] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Reconciliation Alerts" }), reconciliation.findings.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No reconciliation alerts detected" })) : (reconciliation.findings.map((finding, idx) => (_jsxs("div", { style: {
                                                    ...row,
                                                    borderColor: finding.severity === "high" ? "#ef4444" : "#f59e0b",
                                                    background: finding.severity === "high" ? "rgba(127,29,29,0.22)" : "rgba(120,53,15,0.22)",
                                                }, children: [_jsx("div", { style: { fontWeight: 800 }, children: finding.title }), _jsx("div", { style: { marginTop: 6 }, children: finding.detail }), _jsxs("div", { style: { marginTop: 6, opacity: 0.8 }, children: ["Severity: ", finding.severity, " \u2022 Type: ", finding.type] })] }, idx))))] })] })) : (_jsx("div", { style: { opacity: 0.8 }, children: "Medication reconciliation not loaded yet" }))] }), _jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Drug Intelligence Engine" }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("input", { style: input, placeholder: "Search medication name", value: search, onChange: (e) => setSearch(e.target.value) }), _jsx("button", { style: button, onClick: searchDrug, children: "Search" })] }), intelError ? _jsx("div", { style: { color: "#fca5a5", marginTop: 12 }, children: intelError }) : null, intel ? (_jsxs("div", { style: { marginTop: 20, display: "grid", gap: 18 }, children: [_jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "RxNorm Standard Matches" }), rxConcepts.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No RxNorm matches" })) : (rxConcepts.slice(0, 10).map((item, idx) => (_jsxs("div", { style: row, children: [_jsx("strong", { children: item.name || "-" }), _jsxs("div", { children: ["RXCUI: ", item.rxcui || "-"] }), _jsxs("div", { children: ["TTY: ", item.tty || "-"] })] }, idx))))] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Official Drug Snapshot" }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Brand:" }), " ", brandName] }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Generic:" }), " ", genericName] }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Route:" }), " ", routeNames] }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Dosage Form:" }), " ", dosageForm] }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Manufacturer:" }), " ", manufacturer] }), _jsxs("div", { style: row, children: [_jsx("strong", { children: "Active Ingredient:" }), " ", activeIngredient] })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Indications" }), _jsx("div", { style: textBlock, children: indications })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Dose Guidance" }), _jsx("div", { style: textBlock, children: dosageInfo })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Warnings" }), _jsx("div", { style: textBlock, children: warnings })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Contraindications / Do Not Use" }), _jsx("div", { style: textBlock, children: doNotUse })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Ask Doctor Before Use" }), _jsx("div", { style: textBlock, children: askDoctor })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Ask Doctor or Pharmacist" }), _jsx("div", { style: textBlock, children: askPharmacist })] }), _jsxs("div", { style: section, children: [_jsx("div", { style: subTitle, children: "Stop Use" }), _jsx("div", { style: textBlock, children: stopUse })] })] })) : null] }), _jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Unsafe Combinations" }), _jsx("div", { style: { display: "grid", gap: 12 }, children: interactionData?.findings?.length ? (interactionData.findings.map((finding, idx) => (_jsxs("div", { style: {
                                        ...row,
                                        borderColor: finding.severity === "high" ? "#ef4444" : "#f59e0b",
                                        background: finding.severity === "high" ? "rgba(127,29,29,0.22)" : "rgba(120,53,15,0.22)",
                                    }, children: [_jsx("div", { style: { fontWeight: 800 }, children: finding.title }), _jsx("div", { style: { marginTop: 6 }, children: finding.detail }), _jsxs("div", { style: { marginTop: 6, opacity: 0.8 }, children: ["Severity: ", finding.severity, " \u2022 Type: ", finding.type] })] }, idx)))) : (_jsx("div", { style: { opacity: 0.8 }, children: "No unsafe combinations detected" })) })] }), _jsxs("div", { style: card, children: [_jsx("h2", { style: title, children: "Medication Administration Record" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr)) auto", gap: 10 }, children: [_jsx("input", { style: input, placeholder: "Medication", value: medication, onChange: e => setMedication(e.target.value) }), _jsx("input", { style: input, placeholder: "Dose", value: dose, onChange: e => setDose(e.target.value) }), _jsx("input", { style: input, placeholder: "Route", value: route, onChange: e => setRoute(e.target.value) }), _jsx("input", { style: input, placeholder: "Schedule", value: schedule, onChange: e => setSchedule(e.target.value) }), _jsx("button", { style: button, onClick: createItem, children: "Add" })] }), _jsxs("div", { style: { marginTop: 18, display: "grid", gap: 10 }, children: [items.map((i) => (_jsxs("div", { style: row, children: [_jsx("div", { children: _jsx("strong", { children: i.medication }) }), _jsxs("div", { children: ["Dose: ", i.dose] }), _jsxs("div", { children: ["Route: ", i.route] }), _jsxs("div", { children: ["Schedule: ", i.schedule] }), _jsxs("div", { children: ["Status: ", i.status] }), _jsxs("div", { children: ["Given At: ", i.givenAt || "-"] }), _jsxs("div", { children: ["Reviewed At: ", i.reviewedAt || "-"] }), _jsxs("div", { children: ["Pharmacist Note: ", i.pharmacistNote || "-"] }), _jsxs("div", { style: { display: "flex", gap: 8, marginTop: 8 }, children: [_jsx("button", { style: miniButton, onClick: () => give(i.id), children: "Give" }), _jsx("button", { style: dangerButton, onClick: () => remove(i.id), children: "Delete" })] })] }, i.id))), items.length === 0 ? _jsx("div", { style: { opacity: 0.8 }, children: "No MAR items" }) : null] })] })] })] }));
}
const card = {
    border: "1px solid #243041",
    borderRadius: 16,
    padding: 18,
    background: "#111827",
};
const section = {
    border: "1px solid #243041",
    borderRadius: 12,
    padding: 14,
    background: "#0f172a",
};
const badge = {
    padding: "10px 14px",
    borderRadius: 10,
    background: "#0f172a",
    border: "1px solid #334155",
    color: "#93c5fd",
    fontWeight: 700,
};
const title = {
    margin: "0 0 12px 0",
    fontSize: 22,
};
const subTitle = {
    fontSize: 16,
    fontWeight: 700,
    marginBottom: 10,
    color: "#93c5fd",
};
const input = {
    padding: "12px 14px",
    borderRadius: 10,
    border: "1px solid #334155",
    background: "#0f172a",
    color: "white",
};
const button = {
    padding: "12px 16px",
    borderRadius: 10,
    border: "none",
    background: "#0ea5e9",
    color: "white",
    cursor: "pointer",
};
const miniButton = {
    padding: "8px 12px",
    borderRadius: 8,
    border: "none",
    background: "#22c55e",
    color: "white",
    cursor: "pointer",
};
const dangerButton = {
    padding: "8px 12px",
    borderRadius: 8,
    border: "none",
    background: "#ef4444",
    color: "white",
    cursor: "pointer",
};
const reviewButton = {
    padding: "10px 14px",
    borderRadius: 10,
    border: "none",
    background: "#0ea5e9",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
const holdButton = {
    padding: "10px 14px",
    borderRadius: 10,
    border: "none",
    background: "#ef4444",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
const pharmacistButton = {
    padding: "10px 14px",
    borderRadius: 10,
    border: "none",
    background: "#f59e0b",
    color: "white",
    cursor: "pointer",
    fontWeight: 700,
};
const row = {
    border: "1px solid #243041",
    borderRadius: 12,
    padding: 12,
    background: "#0f172a",
};
const textBlock = {
    whiteSpace: "pre-wrap",
    lineHeight: 1.7,
    color: "#e5e7eb",
};
