import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import hospitalLogo from "../assets/hospital-logo.png";
import { apiGet } from "@/lib/api";
const exportClinicalPDF = () => {
    const element = document.getElementById("clinical-report");
    if (!element) {
        alert("Clinical report not found");
        return;
    }
    const printWindow = window.open("", "_blank", "width=1100,height=1400");
    if (!printWindow) {
        alert("Popup blocked. Please allow popups.");
        return;
    }
    printWindow.document.write(`
    <html>
      <head>
        <title>Clinical Report</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 24px;
            color: #111827;
            background: white;
          }
          #print-root {
            width: 100%;
          }
          .avoid-break {
            page-break-inside: avoid;
            break-inside: avoid;
          }
          @media print {
            body {
              margin: 0;
              padding: 14px;
            }
          }
        </style>
      </head>
      <body>
        <div id="print-root">${element.innerHTML}</div>
      </body>
    </html>
  `);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
        printWindow.print();
    }, 500);
};
function getMockVitalSigns(patient) {
    const condition = String(patient.condition ?? "").toLowerCase();
    const status = String(patient.status ?? "").toLowerCase();
    if (condition.includes("chest")) {
        return {
            temperature: "37.2 °C",
            bloodPressure: "145/92 mmHg",
            heartRate: "104 bpm",
            oxygenSaturation: "95%",
            respiratoryRate: "22/min",
        };
    }
    if (condition.includes("fever")) {
        return {
            temperature: "38.6 °C",
            bloodPressure: "118/76 mmHg",
            heartRate: "102 bpm",
            oxygenSaturation: "97%",
            respiratoryRate: "20/min",
        };
    }
    if (condition.includes("oxygen") || status.includes("critical")) {
        return {
            temperature: "37.8 °C",
            bloodPressure: "132/84 mmHg",
            heartRate: "110 bpm",
            oxygenSaturation: "89%",
            respiratoryRate: "26/min",
        };
    }
    return {
        temperature: "36.9 °C",
        bloodPressure: "120/80 mmHg",
        heartRate: "78 bpm",
        oxygenSaturation: "98%",
        respiratoryRate: "16/min",
    };
}
function buildClinicalImpression(patient, notes, orders) {
    const department = patient.department ?? "General Medicine";
    const condition = patient.condition ?? "Unspecified condition";
    const hasUrgentOrder = orders.some((o) => String(o.priority ?? "").toLowerCase() === "urgent");
    const hasNotes = notes.length > 0;
    return `Patient is currently under ${department} care with a presenting condition of ${condition}. ${hasNotes
        ? "Clinical notes indicate that the patient has already undergone initial assessment and documentation."
        : "No detailed narrative notes are currently available in the chart."} ${hasUrgentOrder
        ? "At least one urgent clinical order is active and should be prioritized."
        : "Current listed orders appear routine and should continue to be monitored."} Overall, the patient requires continued physician review, monitoring of response to treatment, and reassessment according to clinical workflow.`;
}
function buildRecommendations(patient, orders) {
    const condition = String(patient.condition ?? "").toLowerCase();
    const department = patient.department ?? "Clinical Department";
    const base = [
        "Continue routine clinical monitoring and reassessment.",
        "Review all pending orders and confirm completion status.",
        "Update physician notes after the next clinical evaluation.",
    ];
    if (condition.includes("chest")) {
        base.unshift("Rule out acute cardiac cause and monitor for symptom progression.");
    }
    else if (condition.includes("fever")) {
        base.unshift("Investigate possible infectious source and monitor temperature trend.");
    }
    else if (condition.includes("oxygen")) {
        base.unshift("Closely monitor oxygen saturation and respiratory stability.");
    }
    else {
        base.unshift(`Maintain protocol-based follow-up under ${department}.`);
    }
    if (orders.length === 0) {
        base.push("Consider entering diagnostic or supportive orders if clinically indicated.");
    }
    return base;
}
export default function ReportsPage() {
    const [searchParams] = useSearchParams();
    const patientIdFromUrl = searchParams.get("patientId") ?? "";
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl || "P-1001");
    const [loadingPatients, setLoadingPatients] = useState(true);
    const [loadingReport, setLoadingReport] = useState(true);
    const [error, setError] = useState("");
    const [report, setReport] = useState({
        patientId: "P-1001",
        patientName: "Loading...",
        title: "Official Clinical Summary",
        status: "draft",
        body: "Generating report...",
        hospitalName: "AI Hospital Alliance",
        doctorName: "Dr. Mohammed Al-Fallah, PharmD",
        visitDate: new Date().toLocaleString(),
    });
    const [patient, setPatient] = useState(null);
    const [notes, setNotes] = useState([]);
    const [orders, setOrders] = useState([]);
    const [vitals, setVitals] = useState(null);
    const [clinicalImpression, setClinicalImpression] = useState("");
    const [recommendations, setRecommendations] = useState([]);
    useEffect(() => {
        if (patientIdFromUrl) {
            setSelectedPatientId(patientIdFromUrl);
        }
    }, [patientIdFromUrl]);
    useEffect(() => {
        async function loadPatients() {
            try {
                setLoadingPatients(true);
                const data = await apiGet("/patients");
                const rows = Array.isArray(data) ? data : [];
                setPatients(rows);
                if (rows.length > 0) {
                    setSelectedPatientId((current) => {
                        const exists = rows.some((p) => p.id === current);
                        return exists ? current : rows[0].id;
                    });
                }
            }
            catch (err) {
                console.error(err);
                setError("Failed to load patients list");
                setPatients([]);
            }
            finally {
                setLoadingPatients(false);
            }
        }
        loadPatients();
    }, []);
    useEffect(() => {
        let cancelled = false;
        async function loadReport() {
            if (!selectedPatientId)
                return;
            try {
                setLoadingReport(true);
                setError("");
                const draftKey = `AI_REPORT_DRAFT_${selectedPatientId}`;
                const rawDraft = localStorage.getItem(draftKey);
                let parsed = null;
                if (rawDraft) {
                    try {
                        parsed = JSON.parse(rawDraft);
                    }
                    catch (err) {
                        console.error("Invalid patient draft:", err);
                    }
                }
                const [currentPatient, currentNotes, currentOrders] = await Promise.all([
                    apiGet(`/patients/${selectedPatientId}`),
                    apiGet(`/notes/${selectedPatientId}`),
                    apiGet(`/orders/${selectedPatientId}`),
                ]);
                if (cancelled)
                    return;
                const safeNotes = Array.isArray(currentNotes) ? currentNotes : [];
                const safeOrders = Array.isArray(currentOrders) ? currentOrders : [];
                setPatient(currentPatient);
                setNotes(safeNotes);
                setOrders(safeOrders);
                const currentVitals = getMockVitalSigns(currentPatient);
                const currentImpression = buildClinicalImpression(currentPatient, safeNotes, safeOrders);
                const currentRecommendations = buildRecommendations(currentPatient, safeOrders);
                setVitals(currentVitals);
                setClinicalImpression(currentImpression);
                setRecommendations(currentRecommendations);
                setReport({
                    patientId: parsed?.patientId ?? currentPatient.id,
                    patientName: parsed?.patientName ?? currentPatient.name,
                    title: parsed?.title ?? "Official Clinical Summary",
                    status: parsed?.status ?? (parsed ? "official-draft" : "auto-generated"),
                    body: parsed?.body ?? currentImpression,
                    hospitalName: parsed?.hospitalName ?? "AI Hospital Alliance",
                    doctorName: parsed?.doctorName ?? "Dr. Mohammed Al-Fallah, PharmD",
                    visitDate: parsed?.visitDate ?? new Date().toLocaleString(),
                });
            }
            catch (err) {
                console.error(err);
                if (cancelled)
                    return;
                setError("Failed to generate report");
                setPatient(null);
                setNotes([]);
                setOrders([]);
                setVitals(null);
                setClinicalImpression("");
                setRecommendations([]);
            }
            finally {
                if (!cancelled) {
                    setLoadingReport(false);
                }
            }
        }
        loadReport();
        return () => {
            cancelled = true;
        };
    }, [selectedPatientId]);
    return (_jsxs("div", { style: { padding: 24, color: "white" }, children: [_jsx("h1", { style: { fontSize: 30, marginBottom: 8 }, children: "Reports" }), _jsx("p", { style: { opacity: 0.8, marginBottom: 20 }, children: "Official clinical and AI-generated reports" }), _jsxs("div", { style: {
                    display: "flex",
                    gap: 12,
                    alignItems: "center",
                    flexWrap: "wrap",
                    marginBottom: 20,
                }, children: [_jsx("select", { value: selectedPatientId, onChange: (e) => setSelectedPatientId(e.target.value), disabled: loadingPatients || patients.length === 0, style: {
                            minWidth: 280,
                            padding: "10px 12px",
                            borderRadius: 8,
                            border: "1px solid #374151",
                            background: "#0f172a",
                            color: "white",
                        }, children: patients.length === 0 ? (_jsx("option", { value: "", children: "No patients available" })) : (patients.map((p) => (_jsxs("option", { value: p.id, children: [p.name, " (", p.id, ")"] }, p.id)))) }), _jsx("button", { onClick: exportClinicalPDF, style: {
                            background: "#2563eb",
                            color: "#fff",
                            padding: "10px 16px",
                            borderRadius: 8,
                            border: "none",
                            cursor: "pointer",
                            fontWeight: 700,
                        }, children: "Print / Save PDF" })] }), error && (_jsx("div", { style: { color: "#fecaca", marginBottom: 16 }, children: error })), _jsxs("div", { id: "clinical-report", style: {
                    background: "white",
                    color: "#111827",
                    borderRadius: 18,
                    padding: 28,
                    maxWidth: 1000,
                    boxShadow: "0 12px 30px rgba(15, 23, 42, 0.12)",
                }, children: [_jsxs("div", { className: "avoid-break", style: {
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            borderBottom: "3px solid #dbeafe",
                            paddingBottom: 18,
                            marginBottom: 24,
                            gap: 16,
                        }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 16 }, children: [_jsx("img", { src: hospitalLogo, alt: "Hospital Logo", style: { height: 64, width: 64, objectFit: "contain" } }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 28, fontWeight: 800, color: "#0f172a" }, children: report.hospitalName }), _jsx("div", { style: { color: "#475569", fontSize: 15 }, children: "Advanced Clinical Decision Report" })] })] }), _jsxs("div", { style: {
                                    textAlign: "right",
                                    fontSize: 14,
                                    background: "#f8fafc",
                                    border: "1px solid #e2e8f0",
                                    borderRadius: 12,
                                    padding: 12,
                                    minWidth: 240,
                                }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Doctor:" }), " ", report.doctorName] }), _jsxs("div", { children: [_jsx("strong", { children: "Date:" }), " ", report.visitDate] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", report.status] })] })] }), _jsxs("div", { className: "avoid-break", style: { marginBottom: 22 }, children: [_jsx("div", { style: { fontSize: 24, fontWeight: 800, marginBottom: 6 }, children: report.title }), _jsxs("div", { style: { color: "#475569" }, children: ["Patient: ", report.patientName, " (", report.patientId, ")"] })] }), _jsxs("div", { className: "avoid-break", style: {
                            display: "grid",
                            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                            gap: 14,
                            marginBottom: 22,
                        }, children: [_jsxs("div", { style: {
                                    background: "#f8fafc",
                                    border: "1px solid #e2e8f0",
                                    borderRadius: 14,
                                    padding: 16,
                                }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, color: "#0f172a" }, children: "Patient Overview" }), _jsxs("div", { style: { display: "grid", gap: 8, fontSize: 14 }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Name:" }), " ", patient?.name ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "ID:" }), " ", patient?.id ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Age:" }), " ", patient?.age ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Gender:" }), " ", patient?.gender ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Phone:" }), " ", patient?.phone ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Department:" }), " ", patient?.department ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Condition:" }), " ", patient?.condition ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", patient?.status ?? "—"] })] })] }), _jsxs("div", { style: {
                                    background: "#eff6ff",
                                    border: "1px solid #bfdbfe",
                                    borderRadius: 14,
                                    padding: 16,
                                }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, color: "#1d4ed8" }, children: "Vital Signs" }), _jsxs("div", { style: { display: "grid", gap: 10, fontSize: 14 }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Temperature:" }), " ", vitals?.temperature ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Blood Pressure:" }), " ", vitals?.bloodPressure ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Heart Rate:" }), " ", vitals?.heartRate ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "O\u2082 Saturation:" }), " ", vitals?.oxygenSaturation ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Respiratory Rate:" }), " ", vitals?.respiratoryRate ?? "—"] })] })] })] }), _jsxs("div", { className: "avoid-break", style: {
                            background: "#f8fafc",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 18,
                            marginBottom: 18,
                        }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, fontSize: 18 }, children: "Clinical Notes" }), _jsx("div", { style: { display: "grid", gap: 10 }, children: loadingReport ? (_jsx("div", { children: "Loading notes..." })) : notes.length === 0 ? (_jsx("div", { children: "No clinical notes recorded." })) : (notes.map((note) => (_jsx("div", { style: {
                                        background: "white",
                                        border: "1px solid #e5e7eb",
                                        borderRadius: 10,
                                        padding: 12,
                                        lineHeight: 1.6,
                                    }, children: note.text }, note.id)))) })] }), _jsxs("div", { className: "avoid-break", style: {
                            background: "#f8fafc",
                            border: "1px solid #e5e7eb",
                            borderRadius: 14,
                            padding: 18,
                            marginBottom: 18,
                        }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, fontSize: 18 }, children: "Clinical Orders" }), _jsx("div", { style: { display: "grid", gap: 10 }, children: loadingReport ? (_jsx("div", { children: "Loading orders..." })) : orders.length === 0 ? (_jsx("div", { children: "No clinical orders recorded." })) : (orders.map((order) => (_jsxs("div", { style: {
                                        display: "grid",
                                        gridTemplateColumns: "minmax(0, 1.5fr) repeat(3, minmax(0, 1fr))",
                                        gap: 10,
                                        background: "white",
                                        border: "1px solid #e5e7eb",
                                        borderRadius: 10,
                                        padding: 12,
                                        fontSize: 14,
                                    }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Item:" }), " ", order.item] }), _jsxs("div", { children: [_jsx("strong", { children: "Type:" }), " ", order.type ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Priority:" }), " ", order.priority ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", order.status ?? "—"] })] }, order.id)))) })] }), _jsxs("div", { className: "avoid-break", style: {
                            background: "#fff7ed",
                            border: "1px solid #fed7aa",
                            borderRadius: 14,
                            padding: 18,
                            marginBottom: 18,
                        }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, fontSize: 18, color: "#9a3412" }, children: "Clinical Impression" }), _jsx("div", { style: { lineHeight: 1.8, whiteSpace: "pre-wrap" }, children: loadingReport ? "Generating clinical impression..." : clinicalImpression })] }), _jsxs("div", { className: "avoid-break", style: {
                            marginBottom: 18,
                        }, children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 12, fontSize: 18 }, children: "Recommendation Boxes" }), _jsx("div", { style: {
                                    display: "grid",
                                    gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                                    gap: 12,
                                }, children: recommendations.map((item, index) => (_jsx("div", { style: {
                                        background: index === 0 ? "#ecfeff" : "#f8fafc",
                                        border: index === 0 ? "1px solid #a5f3fc" : "1px solid #e5e7eb",
                                        borderRadius: 14,
                                        padding: 16,
                                        minHeight: 90,
                                        display: "flex",
                                        alignItems: "flex-start",
                                        lineHeight: 1.6,
                                    }, children: _jsxs("div", { children: [_jsxs("div", { style: {
                                                    fontWeight: 800,
                                                    marginBottom: 6,
                                                    color: index === 0 ? "#0f766e" : "#0f172a",
                                                }, children: ["Recommendation ", index + 1] }), _jsx("div", { children: item })] }) }, index))) })] }), _jsxs("div", { className: "avoid-break", style: {
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "end",
                            marginTop: 34,
                            paddingTop: 22,
                            borderTop: "2px dashed #cbd5e1",
                            gap: 20,
                        }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800, marginBottom: 28 }, children: "Physician Signature: __________________________" }), _jsx("div", { children: report.doctorName }), _jsx("div", { style: { color: "#64748b", fontSize: 14 }, children: "Attending Clinical Reviewer" })] }), _jsx("div", { style: {
                                    border: "2px solid #93c5fd",
                                    color: "#1d4ed8",
                                    borderRadius: "999px",
                                    padding: "10px 18px",
                                    fontWeight: 800,
                                    fontSize: 14,
                                }, children: "VERIFIED HOSPITAL COPY" })] }), _jsx("div", { style: {
                            marginTop: 28,
                            fontSize: 12,
                            color: "#64748b",
                            textAlign: "center",
                        }, children: "AI Hospital Alliance \u2022 Confidential Medical Document \u2022 Auto-generated clinical decision support format" })] })] }));
}
