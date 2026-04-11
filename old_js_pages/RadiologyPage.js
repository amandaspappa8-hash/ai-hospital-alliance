import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet, apiPost } from "@/lib/api";
const OHIF_BASE = "http://127.0.0.1:3005";
const DEMO_STUDY_UID = "1.2.826.0.1.3680043.8.498.40352611434452298538894524161059434702";
export default function RadiologyPage() {
    const [searchParams] = useSearchParams();
    const patientIdFromUrl = searchParams.get("patientId") ?? "";
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState("");
    const [orders, setOrders] = useState([]);
    const [catalog, setCatalog] = useState({});
    const [pacsStudies, setPacsStudies] = useState([]);
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [viewerStudyUid, setViewerStudyUid] = useState(DEMO_STUDY_UID);
    const [form, setForm] = useState({
        section: "xray",
        studies: "",
        priority: "Routine",
    });
    useEffect(() => {
        if (!successMessage)
            return;
        const t = setTimeout(() => setSuccessMessage(""), 2500);
        return () => clearTimeout(t);
    }, [successMessage]);
    useEffect(() => {
        Promise.all([
            apiGet("/patients"),
            apiGet("/radiology/catalog"),
            apiGet("/radiology/orders"),
            apiGet("/pacs/studies"),
        ])
            .then(([p, c, o, pacs]) => {
            const patientsList = Array.isArray(p) ? p : [];
            setPatients(patientsList);
            if (patientIdFromUrl && patientsList.some((patient) => patient.id === patientIdFromUrl)) {
                setSelectedPatientId(patientIdFromUrl);
            }
            else if (patientsList.length > 0) {
                setSelectedPatientId(patientsList[0].id);
            }
            setCatalog((c || {}));
            setOrders(Array.isArray(o) ? o : []);
            setPacsStudies(Array.isArray(pacs) ? pacs : []);
        })
            .catch(() => setError("Failed to load radiology data"));
    }, [patientIdFromUrl]);
    const selectedPatient = useMemo(() => patients.find((p) => p.id === selectedPatientId), [patients, selectedPatientId]);
    const filteredOrders = useMemo(() => orders.filter((o) => !selectedPatientId || o.patientId === selectedPatientId), [orders, selectedPatientId]);
    const selectedPatientStudy = useMemo(() => pacsStudies.find((study) => study.patientId === selectedPatientId), [pacsStudies, selectedPatientId]);
    useEffect(() => {
        if (selectedPatientStudy?.studyInstanceUID) {
            setViewerStudyUid(selectedPatientStudy.studyInstanceUID);
        }
        else {
            setViewerStudyUid(DEMO_STUDY_UID);
        }
    }, [selectedPatientStudy]);
    const ohifViewerUrl = `${OHIF_BASE}/viewer?StudyInstanceUIDs=${encodeURIComponent(viewerStudyUid)}`;
    const submitOrder = async (e) => {
        e.preventDefault();
        setError("");
        if (!selectedPatient)
            return;
        try {
            await apiPost("/radiology/orders", {
                patientId: selectedPatient.id,
                patientName: selectedPatient.name,
                section: form.section,
                studies: form.studies
                    .split(",")
                    .map((t) => t.trim())
                    .filter(Boolean),
                priority: form.priority,
                status: "Pending",
                studyUid: selectedPatientStudy?.studyInstanceUID || DEMO_STUDY_UID,
            });
            const refreshed = await apiGet("/radiology/orders");
            setOrders(Array.isArray(refreshed) ? refreshed : []);
            setForm({
                section: form.section,
                studies: "",
                priority: "Routine",
            });
            setSuccessMessage("Radiology order added");
        }
        catch {
            setError("Failed to save radiology order");
        }
    };
    const openEmbeddedViewer = (studyUid) => {
        setViewerStudyUid(studyUid || selectedPatientStudy?.studyInstanceUID || DEMO_STUDY_UID);
    };
    const openExternalViewer = (studyUid) => {
        const uid = studyUid || selectedPatientStudy?.studyInstanceUID || DEMO_STUDY_UID;
        window.open(`${OHIF_BASE}/viewer?StudyInstanceUIDs=${encodeURIComponent(uid)}`, "_blank", "noopener,noreferrer");
    };
    return (_jsx("div", { style: pageStyle, children: _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { children: [_jsx("h1", { style: { margin: 0, fontSize: 42, fontWeight: 800 }, children: "Radiology \u2022 PACS Integrated" }), _jsx("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: "Embedded OHIF viewer with real PACS study mapping" })] }), error && _jsx("div", { style: errorStyle, children: error }), successMessage && _jsx("div", { style: successStyle, children: successMessage }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1.05fr 1.95fr", gap: 20 }, children: [_jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Patients" }), _jsx("div", { style: { display: "grid", gap: 14 }, children: patients.map((patient) => (_jsxs("button", { onClick: () => setSelectedPatientId(patient.id), style: {
                                            ...itemStyle,
                                            textAlign: "left",
                                            cursor: "pointer",
                                            border: selectedPatientId === patient.id
                                                ? "1px solid rgba(56,189,248,0.95)"
                                                : "1px solid rgba(148,163,184,0.22)",
                                        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: patient.name }), _jsx("div", { style: { marginTop: 6, color: "#cbd5e1" }, children: patient.id }), _jsxs("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: [patient.department ?? "General", " \u2022 ", patient.condition ?? "-"] })] }, patient.id))) })] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Selected Patient" }), selectedPatient ? (_jsxs("div", { style: { display: "grid", gap: 16 }, children: [_jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Name:" }), " ", selectedPatient.name] }), _jsxs("div", { children: [_jsx("strong", { children: "ID:" }), " ", selectedPatient.id] }), _jsxs("div", { children: [_jsx("strong", { children: "Department:" }), " ", selectedPatient.department ?? "-"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", selectedPatient.status ?? "-"] }), _jsxs("div", { style: { gridColumn: "1 / -1" }, children: [_jsx("strong", { children: "Condition:" }), " ", selectedPatient.condition ?? "-"] }), _jsxs("div", { style: { gridColumn: "1 / -1" }, children: [_jsx("strong", { children: "Mapped Study UID:" }), " ", selectedPatientStudy?.studyInstanceUID ?? "No mapped study"] }), _jsxs("div", { style: { gridColumn: "1 / -1" }, children: [_jsx("strong", { children: "Study Description:" }), " ", selectedPatientStudy?.studyDescription ?? "-"] })] }), _jsxs("div", { style: { display: "flex", gap: 12, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", style: primaryBtn, onClick: () => openEmbeddedViewer(), children: "Open Embedded OHIF" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => openExternalViewer(), children: "Open in New Tab" })] })] })) : (_jsx("div", { children: "No patient selected" }))] }), _jsxs("form", { onSubmit: submitOrder, style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Create Imaging Order" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 2fr 1fr", gap: 10 }, children: [_jsx("select", { value: form.section, onChange: (e) => setForm({ ...form, section: e.target.value }), style: inputStyle, children: Object.keys(catalog).map((section) => (_jsx("option", { value: section, children: section }, section))) }), _jsx("input", { style: inputStyle, placeholder: "Studies separated by commas", value: form.studies, onChange: (e) => setForm({ ...form, studies: e.target.value }) }), _jsxs("select", { value: form.priority, onChange: (e) => setForm({ ...form, priority: e.target.value }), style: inputStyle, children: [_jsx("option", { value: "Routine", children: "Routine" }), _jsx("option", { value: "Urgent", children: "Urgent" })] })] }), catalog[form.section]?.length ? (_jsxs("div", { style: { marginTop: 14, color: "#cbd5e1" }, children: ["Available: ", catalog[form.section].join(" • ")] })) : null, _jsx("div", { style: { marginTop: 14 }, children: _jsx("button", { type: "submit", style: primaryBtn, children: "Add Imaging Order" }) })] }), _jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: {
                                                display: "flex",
                                                justifyContent: "space-between",
                                                gap: 12,
                                                alignItems: "center",
                                                marginBottom: 14,
                                                flexWrap: "wrap",
                                            }, children: [_jsxs("div", { children: [_jsx("h2", { style: { ...titleStyle, marginBottom: 4 }, children: "Integrated OHIF PACS Viewer" }), _jsx("div", { style: { color: "#cbd5e1" }, children: "Embedded radiology viewer inside the hospital system" })] }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => openExternalViewer(), children: "External Backup Viewer" })] }), _jsx("iframe", { title: "OHIF PACS Viewer", src: ohifViewerUrl, style: iframeStyle })] }), _jsxs("div", { style: cardStyle, children: [_jsx("h2", { style: titleStyle, children: "Radiology Orders" }), _jsx("div", { style: { display: "grid", gap: 12 }, children: filteredOrders.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No radiology orders yet" })) : (filteredOrders.map((order) => (_jsxs("div", { style: itemStyle, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: order.patientName }), _jsx("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: order.studies.join(" • ") }), _jsxs("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: ["Section: ", order.section, " \u2022 Priority: ", order.priority] }), _jsxs("div", { style: { marginTop: 8, color: "#93c5fd" }, children: ["Study UID: ", order.studyUid ?? "Not assigned"] }), _jsx("div", { style: { marginTop: 10 }, children: _jsx("span", { style: badgeStyle(order.status), children: order.status }) }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap", marginTop: 12 }, children: [_jsx("button", { type: "button", style: miniPrimaryBtn, onClick: () => openEmbeddedViewer(order.studyUid), children: "Open Inside Page" }), _jsx("button", { type: "button", style: miniSecondaryBtn, onClick: () => openExternalViewer(order.studyUid), children: "Open External" })] }), order.report ? (_jsxs("div", { style: { marginTop: 10, color: "#cbd5e1" }, children: ["Report: ", order.report] })) : null] }, order.id)))) })] })] })] })] }) }));
}
const pageStyle = {
    minHeight: "100vh",
    background: "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
    color: "#f8fafc",
    padding: 24,
};
const cardStyle = {
    background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
    border: "1px solid rgba(96,165,250,0.28)",
    borderRadius: 24,
    padding: 22,
    boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
};
const itemStyle = {
    background: "linear-gradient(180deg, rgba(37,99,235,0.18), rgba(15,23,42,0.30))",
    border: "1px solid rgba(96,165,250,0.26)",
    borderRadius: 18,
    padding: 16,
    boxShadow: "0 8px 18px rgba(0,0,0,0.18)",
};
const inputStyle = {
    width: "100%",
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 14,
    padding: "12px 14px",
    background: "rgba(255,255,255,0.08)",
    color: "#f8fafc",
    outline: "none",
};
const primaryBtn = {
    border: "none",
    borderRadius: 14,
    padding: "12px 18px",
    background: "linear-gradient(135deg, #38bdf8, #2563eb)",
    color: "#ffffff",
    fontWeight: 800,
    cursor: "pointer",
    boxShadow: "0 8px 22px rgba(37,99,235,0.35)",
};
const secondaryBtn = {
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 14,
    padding: "12px 18px",
    background: "rgba(255,255,255,0.06)",
    color: "#f8fafc",
    fontWeight: 700,
    cursor: "pointer",
};
const miniPrimaryBtn = {
    border: "none",
    borderRadius: 10,
    padding: "9px 12px",
    background: "#38bdf8",
    color: "#082f49",
    fontWeight: 800,
    cursor: "pointer",
};
const miniSecondaryBtn = {
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 10,
    padding: "9px 12px",
    background: "rgba(255,255,255,0.06)",
    color: "#f8fafc",
    fontWeight: 700,
    cursor: "pointer",
};
const iframeStyle = {
    width: "100%",
    height: "78vh",
    border: "1px solid rgba(96,165,250,0.22)",
    borderRadius: 18,
    background: "#020617",
};
const titleStyle = {
    margin: "0 0 14px 0",
    fontSize: 22,
    fontWeight: 800,
};
const errorStyle = {
    background: "rgba(239,68,68,0.18)",
    border: "1px solid rgba(248,113,113,0.4)",
    color: "#fecaca",
    borderRadius: 16,
    padding: "14px 16px",
};
const successStyle = {
    background: "rgba(34,197,94,0.16)",
    border: "1px solid rgba(74,222,128,0.35)",
    color: "#bbf7d0",
    borderRadius: 16,
    padding: "14px 16px",
};
const badgeStyle = (status) => ({
    display: "inline-flex",
    alignItems: "center",
    padding: "8px 12px",
    borderRadius: 999,
    fontWeight: 800,
    fontSize: 13,
    background: status === "Completed"
        ? "rgba(34,197,94,0.18)"
        : status === "Pending"
            ? "rgba(250,204,21,0.16)"
            : "rgba(59,130,246,0.16)",
    color: status === "Completed"
        ? "#86efac"
        : status === "Pending"
            ? "#fde68a"
            : "#93c5fd",
    border: status === "Completed"
        ? "1px solid rgba(74,222,128,0.35)"
        : status === "Pending"
            ? "1px solid rgba(250,204,21,0.3)"
            : "1px solid rgba(96,165,250,0.35)",
});
