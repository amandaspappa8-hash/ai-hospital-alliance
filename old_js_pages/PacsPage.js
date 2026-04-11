import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { apiGet } from "@/lib/api";
const OHIF_BASE = "http://127.0.0.1:3005";
export default function PacsPage() {
    const [studies, setStudies] = useState([]);
    const [selectedUid, setSelectedUid] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        apiGet("/pacs/studies")
            .then((data) => {
            const rows = Array.isArray(data) ? data : [];
            setStudies(rows);
            if (rows.length > 0) {
                setSelectedUid(rows[0].studyInstanceUID);
            }
        })
            .catch((err) => {
            console.error(err);
            setError("Failed to load PACS studies from backend");
        })
            .finally(() => setLoading(false));
    }, []);
    const selected = useMemo(() => studies.find((study) => study.studyInstanceUID === selectedUid) || null, [studies, selectedUid]);
    const openOhif = (studyUid) => {
        const uid = studyUid || selected?.studyInstanceUID;
        if (!uid)
            return;
        window.open(`${OHIF_BASE}/viewer?StudyInstanceUIDs=${encodeURIComponent(uid)}`, "_blank", "noopener,noreferrer");
    };
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "28px", marginBottom: "8px" }, children: "PACS" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Real Orthanc studies via backend PACS proxy" }), loading && _jsx("div", { children: "Loading studies..." }), error && _jsx("div", { style: { color: "#fca5a5" }, children: error }), !loading && !error && (_jsxs(_Fragment, { children: [_jsx("div", { style: {
                            overflowX: "auto",
                            border: "1px solid #374151",
                            borderRadius: "12px",
                            marginBottom: "20px",
                        }, children: _jsxs("table", { style: { width: "100%", borderCollapse: "collapse" }, children: [_jsx("thead", { style: { background: "#111827" }, children: _jsxs("tr", { children: [_jsx("th", { style: th, children: "Patient" }), _jsx("th", { style: th, children: "Patient ID" }), _jsx("th", { style: th, children: "Modality" }), _jsx("th", { style: th, children: "Date" }), _jsx("th", { style: th, children: "Description" }), _jsx("th", { style: th, children: "Study UID" }), _jsx("th", { style: th, children: "Action" })] }) }), _jsxs("tbody", { children: [studies.map((study) => (_jsxs("tr", { style: {
                                                background: selectedUid === study.studyInstanceUID ? "#0f172a" : "transparent",
                                            }, children: [_jsx("td", { style: td, children: study.patientName || "-" }), _jsx("td", { style: td, children: study.patientId || "-" }), _jsx("td", { style: td, children: study.modality || "-" }), _jsx("td", { style: td, children: study.studyDate || "-" }), _jsx("td", { style: td, children: study.studyDescription || "-" }), _jsx("td", { style: td, children: study.studyInstanceUID }), _jsx("td", { style: td, children: _jsx("button", { onClick: () => setSelectedUid(study.studyInstanceUID), style: {
                                                            padding: "8px 12px",
                                                            borderRadius: "8px",
                                                            border: "1px solid #374151",
                                                            background: selectedUid === study.studyInstanceUID ? "#166534" : "#111827",
                                                            color: "white",
                                                            cursor: "pointer",
                                                        }, children: "Open" }) })] }, study.studyInstanceUID))), studies.length === 0 && (_jsx("tr", { children: _jsx("td", { style: td, colSpan: 7, children: "No PACS studies found" }) }))] })] }) }), selected && (_jsxs("div", { style: {
                            border: "1px solid #374151",
                            borderRadius: "12px",
                            padding: "16px",
                            background: "#111827",
                        }, children: [_jsx("div", { style: { fontSize: "20px", fontWeight: 700, marginBottom: "10px" }, children: "Selected Study" }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Patient:" }), " ", selected.patientName || "-"] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Patient ID:" }), " ", selected.patientId || "-"] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Modality:" }), " ", selected.modality || "-"] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Date:" }), " ", selected.studyDate || "-"] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Description:" }), " ", selected.studyDescription || "-"] }), _jsxs("div", { style: { marginBottom: "8px", wordBreak: "break-all" }, children: [_jsx("strong", { children: "Study UID:" }), " ", selected.studyInstanceUID] }), _jsx("div", { style: { marginTop: "20px" }, children: _jsx("button", { onClick: () => openOhif(selected.studyInstanceUID), style: {
                                        padding: "12px 20px",
                                        borderRadius: "10px",
                                        background: "#0ea5e9",
                                        border: "none",
                                        color: "white",
                                        fontSize: "16px",
                                        cursor: "pointer",
                                    }, children: "Open Study in OHIF Viewer" }) })] }))] }))] }));
}
const th = {
    textAlign: "left",
    padding: "12px",
    borderBottom: "1px solid #374151",
};
const td = {
    padding: "12px",
    borderBottom: "1px solid #1f2937",
};
