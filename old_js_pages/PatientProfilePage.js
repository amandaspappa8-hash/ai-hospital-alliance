import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiGet, apiPost } from "@/lib/api";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import QRCode from "qrcode";
export default function PatientProfilePage() {
    const openPatientPacs = (studyUid) => {
        const uid = patientPacsStudy?.studyInstanceUID ||
            studyUid ||
            latestRadiologyOrder?.studyUid ||
            "";
        if (!uid) {
            alert("No PACS study mapped for this patient yet");
            window.location.href = `/radiology?patientId=${selectedId}`;
            return;
        }
        window.open(`http://127.0.0.1:3005/viewer?StudyInstanceUIDs=${encodeURIComponent(uid)}`, "_blank", "noopener,noreferrer");
    };
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const patientIdFromUrl = searchParams.get("id") ?? "";
    const [patients, setPatients] = useState([]);
    const [selectedId, setSelectedId] = useState("");
    const [q, setQ] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [tab, setTab] = useState("overview");
    const [notes, setNotes] = useState([]);
    const [noteText, setNoteText] = useState("");
    const [savingNote, setSavingNote] = useState(false);
    const [orders, setOrders] = useState([]);
    const [labOrders, setLabOrders] = useState([]);
    const [radiologyOrders, setRadiologyOrders] = useState([]);
    const [pacsStudies, setPacsStudies] = useState([]);
    const [chiefComplaint, setChiefComplaint] = useState("chest pain");
    const [symptomsText, setSymptomsText] = useState("sweating, nausea, shortness of breath");
    const [ageInput, setAgeInput] = useState("58");
    const [genderInput, setGenderInput] = useState("male");
    const [aiLoading, setAiLoading] = useState(false);
    const [aiError, setAiError] = useState("");
    const [aiResult, setAiResult] = useState(null);
    const [qrCode, setQrCode] = useState("");
    const [visitId, setVisitId] = useState("");
    const generateOfficialReport = async () => {
        if (!selected)
            return;
        try {
            const notesData = await apiGet(`/notes/${selected.id}`);
            const ordersData = await apiGet(`/orders/${selected.id}`);
            const currentLabOrders = await apiGet(`/labs/orders/${selected.id}`);
            const currentRadiologyOrders = await apiGet(`/radiology/orders/${selected.id}`);
            const notesText = Array.isArray(notesData) && notesData.length > 0
                ? notesData.map((n) => `- ${n.text}`).join("\n")
                : "No clinical notes recorded.";
            const ordersText = Array.isArray(ordersData) && ordersData.length > 0
                ? ordersData
                    .map((o) => `- ${o.item} | Type: ${o.type ?? "N/A"} | Priority: ${o.priority ?? "N/A"} | Status: ${o.status ?? "Pending"}`)
                    .join("\n")
                : "No clinical orders recorded.";
            const labText = Array.isArray(currentLabOrders) && currentLabOrders.length > 0
                ? currentLabOrders
                    .map((o) => `- ${o.tests.join(", ")} | ${o.section} | ${o.priority} | ${o.status} | Result: ${o.result || "N/A"}`)
                    .join("\n")
                : "No lab orders recorded.";
            const radiologyText = Array.isArray(currentRadiologyOrders) && currentRadiologyOrders.length > 0
                ? currentRadiologyOrders
                    .map((o) => `- ${o.studies.join(", ")} | ${o.section} | ${o.priority} | ${o.status} | Report: ${o.report || "N/A"}`)
                    .join("\n")
                : "No radiology orders recorded.";
            const body = `Patient Name: ${selected.name}
Patient ID: ${selected.id}
Age: ${selected.age ?? "N/A"}
Gender: ${selected.gender ?? "N/A"}
Phone: ${selected.phone ?? "N/A"}
Condition: ${selected.condition ?? "N/A"}
Department: ${selected.department ?? "N/A"}
Patient Status: ${selected.status ?? "N/A"}

Clinical Notes:
${notesText}

Clinical Orders:
${ordersText}

Laboratory Orders:
${labText}

Radiology Orders:
${radiologyText}

Official Clinical Impression:
This official draft was generated from the patient profile view. It summarizes the currently available chart data, notes, clinical orders, lab orders, and radiology studies for physician review and final validation.`;
            const draft = {
                patientId: selected.id,
                patientName: selected.name,
                title: "Official Clinical Summary",
                status: "official-draft",
                body,
                hospitalName: "AI Hospital Alliance",
                doctorName: "Dr. Mohammed Al-Fallah, PharmD",
                visitDate: new Date().toLocaleString(),
            };
            localStorage.setItem(`AI_REPORT_DRAFT_${selected.id}`, JSON.stringify(draft));
            window.location.href = `/reports?patientId=${selected.id}`;
        }
        catch (err) {
            console.error("Failed to generate official report:", err);
            alert("Failed to generate official report");
        }
    };
    useEffect(() => {
        const id = "VIS-" +
            new Date().getFullYear() +
            "-" +
            Math.floor(Math.random() * 100000);
        setVisitId(id);
        QRCode.toDataURL(id).then((url) => {
            setQrCode(url);
        });
    }, []);
    useEffect(() => {
        apiGet("/patients")
            .then((data) => {
            const rows = Array.isArray(data) ? data : [];
            setPatients(rows);
            if (patientIdFromUrl) {
                setSelectedId(patientIdFromUrl);
            }
            else if (rows.length > 0) {
                setSelectedId(rows[0].id);
            }
        })
            .catch((err) => {
            console.error(err);
            setError("Failed to load patients");
        })
            .finally(() => setLoading(false));
    }, [patientIdFromUrl]);
    const filtered = useMemo(() => {
        const query = q.trim().toLowerCase();
        return patients.filter((p) => {
            return (!query ||
                String(p.id ?? "").toLowerCase().includes(query) ||
                String(p.name ?? "").toLowerCase().includes(query) ||
                String(p.department ?? "").toLowerCase().includes(query) ||
                String(p.condition ?? "").toLowerCase().includes(query));
        });
    }, [patients, q]);
    const selected = patients.find((p) => p.id === selectedId) ||
        filtered[0] ||
        patients[0] ||
        null;
    useEffect(() => {
        if (!selected?.id)
            return;
        setAgeInput(String(selected.age ?? 58));
        setGenderInput(selected.gender ?? "male");
        Promise.all([
            apiGet(`/notes/${selected.id}`).catch(() => []),
            apiGet(`/orders/${selected.id}`).catch(() => []),
            apiGet(`/labs/orders/${selected.id}`).catch(() => []),
            apiGet(`/radiology/orders/${selected.id}`).catch(() => []),
            apiGet("/pacs/studies").catch(() => []),
        ])
            .then(([notesData, ordersData, labData, radiologyData, pacsData]) => {
            setNotes(Array.isArray(notesData) ? notesData : []);
            setOrders(Array.isArray(ordersData) ? ordersData : []);
            setLabOrders(Array.isArray(labData) ? labData : []);
            setRadiologyOrders(Array.isArray(radiologyData) ? radiologyData : []);
            setPacsStudies(Array.isArray(pacsData)
                ? pacsData.filter((study) => study.patientId === selected.id)
                : []);
        })
            .catch((err) => {
            console.error(err);
        });
    }, [selected?.id]);
    const exportClinicalPDF = async () => {
        const input = document.getElementById("clinical-report");
        if (!input)
            return;
        const canvas = await html2canvas(input, { scale: 2 });
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "mm", "a4");
        const imgWidth = 210;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
        pdf.save(`Clinical_Report_${visitId || "report"}.pdf`);
    };
    async function addNote() {
        if (!selected?.id || !noteText.trim())
            return;
        setSavingNote(true);
        try {
            await apiPost(`/notes/${selected.id}`, { text: noteText.trim() });
            const data = await apiGet(`/notes/${selected.id}`);
            setNotes(Array.isArray(data) ? data : []);
            setNoteText("");
        }
        catch (err) {
            console.error(err);
        }
        finally {
            setSavingNote(false);
        }
    }
    async function runAIAndCreateOrders() {
        if (!selected?.id)
            return;
        setAiLoading(true);
        setAiError("");
        try {
            const payload = {
                chief_complaint: chiefComplaint.trim(),
                symptoms: symptomsText.split(",").map((item) => item.trim()).filter(Boolean),
                age: ageInput.trim() ? Number(ageInput) : undefined,
                gender: genderInput.trim() || undefined,
            };
            const result = await apiPost(`/ai/clinical-route-and-create-orders/${selected.id}`, payload);
            setAiResult(result.clinical_route);
            const latestOrders = await apiGet(`/orders/${selected.id}`);
            setOrders(Array.isArray(latestOrders) ? latestOrders : []);
        }
        catch (err) {
            console.error(err);
            setAiError("Failed to create AI draft orders");
        }
        finally {
            setAiLoading(false);
        }
    }
    const latestLabOrder = labOrders[0];
    const latestRadiologyOrder = radiologyOrders.length > 0 ? radiologyOrders[radiologyOrders.length - 1] : null;
    const patientPacsStudy = pacsStudies.find((study) => study.patientId === selectedId) || pacsStudies[0] || null;
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Patient Profile" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Electronic Medical Record workspace" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "320px minmax(0,1fr)", gap: "20px", alignItems: "start" }, children: [_jsxs("div", { style: { background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "16px" }, children: [_jsx("input", { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search patient...", style: inputStyle }), _jsxs("div", { style: { marginTop: "14px" }, children: [loading && _jsx("div", { children: "Loading patients..." }), error && _jsx("div", { style: { color: "#fca5a5" }, children: error }), !loading && !error && filtered.map((p) => {
                                        const active = selected?.id === p.id;
                                        return (_jsxs("div", { onClick: () => setSelectedId(p.id), style: {
                                                padding: "12px",
                                                marginBottom: "10px",
                                                borderRadius: "10px",
                                                cursor: "pointer",
                                                border: "1px solid #374151",
                                                background: active ? "#172033" : "#0b1220",
                                            }, children: [_jsx("div", { style: { fontWeight: 700 }, children: p.name }), _jsxs("div", { style: { opacity: 0.75, fontSize: "14px", marginTop: "4px" }, children: [p.id, " \u2022 ", p.department ?? "General"] })] }, p.id));
                                    })] })] }), _jsx("div", { children: !selected ? (_jsx("div", { children: "No patient selected." })) : (_jsxs(_Fragment, { children: [_jsxs("div", { style: { background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "20px", marginBottom: "18px" }, children: [_jsx("div", { style: { fontSize: "28px", fontWeight: 700 }, children: selected.name }), _jsxs("div", { style: { opacity: 0.8, marginTop: "6px" }, children: [selected.id, " \u2022 ", selected.department ?? "General", " \u2022 ", selected.status ?? "Unknown"] }), _jsxs("div", { style: { display: "flex", gap: "10px", flexWrap: "wrap", marginTop: "16px" }, children: [_jsx("button", { onClick: () => navigate(`/clinical-decision?patientId=${selected.id}&complaint=${encodeURIComponent(selected.condition ?? "")}`), style: {
                                                        padding: "12px 18px",
                                                        borderRadius: "10px",
                                                        border: "1px solid #38bdf8",
                                                        background: "#0284c7",
                                                        color: "white",
                                                        cursor: "pointer",
                                                        fontWeight: 700,
                                                    }, children: "Open AI Clinical Decision" }), _jsx("button", { onClick: () => navigate(`/labs?patientId=${selected.id}`), style: {
                                                        padding: "12px 18px",
                                                        borderRadius: "10px",
                                                        border: "1px solid #22c55e",
                                                        background: "#166534",
                                                        color: "white",
                                                        cursor: "pointer",
                                                        fontWeight: 700,
                                                    }, children: "Open Labs" }), _jsx("button", { onClick: () => navigate(`/radiology?patientId=${selected.id}`), style: {
                                                        padding: "12px 18px",
                                                        borderRadius: "10px",
                                                        border: "1px solid #06b6d4",
                                                        background: "#0e7490",
                                                        color: "white",
                                                        cursor: "pointer",
                                                        fontWeight: 700,
                                                    }, children: "Open Radiology" })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "12px", marginTop: "18px" }, children: [_jsx(InfoCard, { label: "Age", value: selected.age ?? "N/A" }), _jsx(InfoCard, { label: "Gender", value: selected.gender ?? "N/A" }), _jsx(InfoCard, { label: "Phone", value: selected.phone ?? "N/A" }), _jsx(InfoCard, { label: "Condition", value: selected.condition ?? "No active note" })] })] }), _jsxs("div", { style: { display: "flex", gap: "10px", marginBottom: "18px", flexWrap: "wrap" }, children: [_jsx(TabButton, { active: tab === "overview", onClick: () => setTab("overview"), children: "Overview" }), _jsx(TabButton, { active: tab === "notes", onClick: () => setTab("notes"), children: "Notes" }), _jsx(TabButton, { active: tab === "orders", onClick: () => setTab("orders"), children: "Orders" })] }), tab === "overview" && (_jsxs("div", { style: { display: "grid", gap: "18px" }, children: [_jsxs(Panel, { title: "Integrated Clinical Snapshot", children: [_jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))", gap: "12px" }, children: [_jsx(InfoCard, { label: "Manual Orders", value: orders.length }), _jsx(InfoCard, { label: "Lab Orders", value: labOrders.length }), _jsx(InfoCard, { label: "Radiology Orders", value: radiologyOrders.length }), _jsx(InfoCard, { label: "Clinical Notes", value: notes.length })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))", gap: "12px", marginTop: "14px" }, children: [_jsxs("div", { style: cardStyle, children: [_jsx("div", { style: { fontWeight: 700, marginBottom: "8px" }, children: "Latest Lab Result" }), latestLabOrder ? (_jsxs(_Fragment, { children: [_jsx("div", { children: latestLabOrder.tests.join(", ") }), _jsx("div", { style: { opacity: 0.75, marginTop: "6px" }, children: latestLabOrder.status }), _jsx("div", { style: { opacity: 0.85, marginTop: "8px" }, children: latestLabOrder.result || "No result yet" })] })) : (_jsx("div", { style: { opacity: 0.75 }, children: "No lab order yet." }))] }), _jsxs("div", { style: cardStyle, children: [_jsx("div", { style: { fontWeight: 700, marginBottom: "8px" }, children: "Latest Radiology Report" }), latestRadiologyOrder ? (_jsxs(_Fragment, { children: [_jsx("div", { children: latestRadiologyOrder.studies.join(", ") }), _jsx("div", { style: { opacity: 0.75, marginTop: "6px" }, children: latestRadiologyOrder.status }), _jsx("div", { style: { opacity: 0.85, marginTop: "8px" }, children: latestRadiologyOrder.report || "No report yet" })] })) : (_jsx("div", { style: { opacity: 0.75 }, children: "No radiology order yet." }))] })] })] }), _jsx(Panel, { title: "AI Clinical Workflow", children: _jsxs("div", { style: { display: "grid", gap: "12px" }, children: [_jsxs("div", { children: [_jsx("div", { style: labelStyle, children: "Chief Complaint" }), _jsx("input", { value: chiefComplaint, onChange: (e) => setChiefComplaint(e.target.value), style: inputStyle })] }), _jsxs("div", { children: [_jsx("div", { style: labelStyle, children: "Symptoms (comma separated)" }), _jsx("textarea", { value: symptomsText, onChange: (e) => setSymptomsText(e.target.value), style: textareaStyle })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: "12px" }, children: [_jsxs("div", { children: [_jsx("div", { style: labelStyle, children: "Age" }), _jsx("input", { value: ageInput, onChange: (e) => setAgeInput(e.target.value), style: inputStyle })] }), _jsxs("div", { children: [_jsx("div", { style: labelStyle, children: "Gender" }), _jsx("input", { value: genderInput, onChange: (e) => setGenderInput(e.target.value), style: inputStyle })] })] }), _jsx("button", { onClick: runAIAndCreateOrders, style: buttonStyle, children: aiLoading ? "Processing..." : "Run AI + Create Draft Orders" }), aiError && _jsx("div", { style: { color: "#fca5a5" }, children: aiError })] }) }), aiResult && (_jsxs(_Fragment, { children: [_jsx(Panel, { title: "AI Triage Result", children: _jsxs("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: "12px" }, children: [_jsx(InfoCard, { label: "Triage Level", value: aiResult.triage_level }), _jsx(InfoCard, { label: "Urgency Score", value: aiResult.urgency_score }), _jsx(InfoCard, { label: "Chief Complaint", value: aiResult.chief_complaint })] }) }), _jsx(Panel, { title: "Route To", children: _jsx("div", { style: { display: "flex", gap: "10px", flexWrap: "wrap" }, children: aiResult.route_to.map((item) => (_jsx("span", { style: pillStyle, children: item }, item))) }) }), _jsx(Panel, { title: "Suggested Orders", children: _jsx("div", { style: { display: "grid", gap: "10px" }, children: aiResult.suggested_orders.map((item) => (_jsxs("div", { style: cardStyle, children: [_jsx("div", { style: { fontWeight: 700 }, children: item.name }), _jsxs("div", { style: { opacity: 0.8, marginTop: "4px" }, children: [item.priority, " \u2022 ", item.category] })] }, item.name))) }) })] })), _jsxs(Panel, { title: "Clinical Report PDF", children: [_jsx("button", { onClick: exportClinicalPDF, style: buttonStyle, children: "Export Clinical Report PDF" }), _jsxs("div", { id: "clinical-report", style: {
                                                        marginTop: "18px",
                                                        background: "white",
                                                        color: "#111827",
                                                        padding: "40px",
                                                        borderRadius: "12px",
                                                        position: "relative",
                                                        width: "800px",
                                                        maxWidth: "100%",
                                                        overflow: "hidden",
                                                    }, children: [_jsx("div", { style: {
                                                                position: "absolute",
                                                                top: "38%",
                                                                left: "16%",
                                                                fontSize: "76px",
                                                                color: "#e5e7eb",
                                                                transform: "rotate(-30deg)",
                                                                opacity: 0.3,
                                                                fontWeight: "bold",
                                                                pointerEvents: "none",
                                                            }, children: "AI HOSPITAL" }), _jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", borderBottom: "2px solid #e5e7eb", paddingBottom: "16px" }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontSize: "28px", fontWeight: 800 }, children: "AI Hospital Alliance" }), _jsx("div", { style: { color: "#6b7280", marginTop: "4px" }, children: "Clinical Medical Report" }), _jsxs("div", { style: { color: "#6b7280", marginTop: "4px" }, children: ["Department: ", selected.department ?? "General Medicine"] })] }), _jsxs("div", { style: { textAlign: "right" }, children: [qrCode ? _jsx("img", { src: qrCode, style: { height: 90 } }) : null, _jsx("div", { style: { fontSize: "10px", marginTop: "6px" }, children: "Scan Verification" })] })] }), _jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginTop: "16px", fontSize: "14px" }, children: [_jsxs("div", { children: [_jsx("b", { children: "Visit ID:" }), " ", visitId] }), _jsxs("div", { children: [_jsx("b", { children: "Date:" }), " ", new Date().toLocaleDateString()] })] }), _jsxs("div", { style: {
                                                                display: "grid",
                                                                gridTemplateColumns: "1fr 1fr",
                                                                gap: "30px",
                                                                marginTop: "30px",
                                                            }, children: [_jsxs("div", { children: [_jsxs("p", { children: [_jsx("b", { children: "Patient Name:" }), " ", selected.name] }), _jsxs("p", { children: [_jsx("b", { children: "Age:" }), " ", selected.age ?? "N/A"] }), _jsxs("p", { children: [_jsx("b", { children: "Gender:" }), " ", selected.gender ?? "N/A"] }), _jsxs("p", { children: [_jsx("b", { children: "Phone:" }), " ", selected.phone ?? "N/A"] })] }), _jsxs("div", { children: [_jsxs("p", { children: [_jsx("b", { children: "Department:" }), " ", selected.department ?? "General"] }), _jsxs("p", { children: [_jsx("b", { children: "Status:" }), " ", selected.status ?? "Unknown"] }), _jsxs("p", { children: [_jsx("b", { children: "Condition:" }), " ", selected.condition ?? "N/A"] }), _jsxs("p", { children: [_jsx("b", { children: "Patient ID:" }), " ", selected.id] })] })] }), _jsxs("div", { style: { marginTop: "28px" }, children: [_jsx("div", { style: { fontSize: "18px", fontWeight: 700, marginBottom: "8px" }, children: "Clinical Impression" }), _jsx("div", { style: { lineHeight: 1.7 }, children: aiResult
                                                                        ? `Patient triage level is ${aiResult.triage_level} with urgency score ${aiResult.urgency_score}. Chief complaint: ${aiResult.chief_complaint}.`
                                                                        : "AI generated clinical summary will appear here after running the AI workflow." })] }), _jsxs("div", { style: { marginTop: "24px" }, children: [_jsx("div", { style: { fontSize: "18px", fontWeight: 700, marginBottom: "8px" }, children: "Laboratory Summary" }), _jsx("div", { style: { lineHeight: 1.7 }, children: latestLabOrder
                                                                        ? `${latestLabOrder.tests.join(", ")} — ${latestLabOrder.status} — ${latestLabOrder.result || "No result yet"}`
                                                                        : "No laboratory data yet." })] }), _jsxs("div", { style: { marginTop: "24px" }, children: [_jsx("div", { style: { fontSize: "18px", fontWeight: 700, marginBottom: "8px" }, children: "Radiology Summary" }), _jsx("div", { style: { lineHeight: 1.7 }, children: latestRadiologyOrder
                                                                        ? `${latestRadiologyOrder.studies.join(", ")} — ${latestRadiologyOrder.status} — ${latestRadiologyOrder.report || "No report yet"}`
                                                                        : "No radiology data yet." })] }), _jsxs("div", { style: { marginTop: "60px" }, children: [_jsx("p", { style: { fontSize: 12, color: "#666" }, children: "Doctor Digital Signature" }), _jsx("img", { src: "/assets/sign.png", style: { height: 60, marginTop: 10 }, onError: (e) => {
                                                                        ;
                                                                        e.currentTarget.style.display = "none";
                                                                    } }), _jsx("div", { style: { borderTop: "1px solid #000", width: 220, marginTop: 10 } }), _jsx("p", { style: { fontWeight: "bold", marginTop: 5 }, children: "Dr Mohammed Elfallah" })] })] })] })] })), tab === "notes" && (_jsxs(Panel, { title: "Clinical Notes", children: [_jsx("textarea", { value: noteText, onChange: (e) => setNoteText(e.target.value), placeholder: "Write note for this patient...", style: textareaStyle }), _jsx("button", { onClick: addNote, style: buttonStyle, children: savingNote ? "Saving..." : "Add Note" }), _jsx("div", { style: { marginTop: "18px" }, children: notes.length === 0 ? (_jsx("div", { style: { opacity: 0.75 }, children: "No notes for this patient yet." })) : (_jsx("div", { style: { display: "grid", gap: "10px" }, children: notes.map((note) => (_jsx("div", { style: cardStyle, children: note.text }, note.id))) })) })] })), tab === "orders" && (_jsxs("div", { style: { display: "grid", gap: "18px" }, children: [_jsx(Panel, { title: "Manual Clinical Orders", children: orders.length === 0 ? (_jsx("div", { style: { opacity: 0.75 }, children: "No manual orders for this patient yet." })) : (_jsx("div", { style: { display: "grid", gap: "10px" }, children: orders.map((order) => (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { fontWeight: 700 }, children: ["#", order.id, " \u2014 ", order.type] }), _jsxs("div", { style: { opacity: 0.82, marginTop: "4px" }, children: [order.department, " \u2022 ", order.status] }), order.note && _jsx("div", { style: { opacity: 0.75, marginTop: "6px" }, children: order.note })] }, order.id))) })) }), _jsx(Panel, { title: "Laboratory Orders", children: labOrders.length === 0 ? (_jsx("div", { style: { opacity: 0.75 }, children: "No lab orders for this patient yet." })) : (_jsx("div", { style: { display: "grid", gap: "10px" }, children: labOrders.map((order) => (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { fontWeight: 700 }, children: [order.id, " \u2014 ", order.tests.join(", ")] }), _jsxs("div", { style: { opacity: 0.82, marginTop: "4px" }, children: [order.section, " \u2022 ", order.priority, " \u2022 ", order.status] }), _jsxs("div", { style: { opacity: 0.75, marginTop: "6px" }, children: ["Result: ", order.result || "Not available yet"] })] }, order.id))) })) }), _jsx(Panel, { title: "Radiology Orders", children: radiologyOrders.length === 0 ? (_jsx("div", { style: { opacity: 0.75 }, children: "No radiology orders for this patient yet." })) : (_jsx("div", { style: { display: "grid", gap: "10px" }, children: radiologyOrders.map((order) => (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { fontWeight: 700 }, children: [order.id, " \u2014 ", order.studies.join(", ")] }), _jsxs("div", { style: { opacity: 0.82, marginTop: "4px" }, children: [order.section, " \u2022 ", order.priority, " \u2022 ", order.status] }), _jsxs("div", { style: { opacity: 0.75, marginTop: "6px" }, children: ["Report: ", order.report || "Not available yet"] })] }, order.id))) })) })] }))] })) })] })] }));
}
function TabButton({ active, onClick, children }) {
    return (_jsx("button", { onClick: onClick, style: {
            padding: "10px 14px",
            borderRadius: "10px",
            border: "1px solid #374151",
            background: active ? "#166534" : "#111827",
            color: "white",
            cursor: "pointer",
        }, children: children }));
}
function InfoCard({ label, value }) {
    return (_jsxs("div", { style: { background: "#0b1220", border: "1px solid #374151", borderRadius: "10px", padding: "14px" }, children: [_jsx("div", { style: { opacity: 0.72, fontSize: "14px" }, children: label }), _jsx("div", { style: { marginTop: "8px", fontWeight: 700 }, children: value })] }));
}
function Panel({ title, children }) {
    return (_jsxs("div", { style: { background: "#111827", border: "1px solid #374151", borderRadius: "12px", padding: "16px" }, children: [_jsx("div", { style: { fontSize: "18px", fontWeight: 700, marginBottom: "12px" }, children: title }), children] }));
}
const inputStyle = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const textareaStyle = {
    width: "100%",
    minHeight: "120px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const buttonStyle = {
    padding: "12px 18px",
    borderRadius: "10px",
    border: "1px solid #22c55e",
    background: "#166534",
    color: "white",
    cursor: "pointer",
    fontWeight: 600,
};
const labelStyle = {
    marginBottom: "6px",
    opacity: 0.8,
    fontSize: "14px",
};
const pillStyle = {
    padding: "8px 12px",
    borderRadius: "999px",
    background: "#166534",
    border: "1px solid #22c55e",
};
const cardStyle = {
    padding: "12px",
    background: "#0b1220",
    border: "1px solid #374151",
    borderRadius: "10px",
};
