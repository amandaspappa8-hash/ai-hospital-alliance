import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
function readValue(item, tag) {
    return item?.[tag]?.Value?.[0];
}
function readPersonName(item, tag) {
    return item?.[tag]?.Value?.[0]?.Alphabetic ?? "-";
}
function mapStudy(item) {
    return {
        studyInstanceUID: readValue(item, "0020000D") ?? "",
        patientName: readPersonName(item, "00100010"),
        patientId: readValue(item, "00100020") ?? "-",
        modality: readValue(item, "00080061") ?? "-",
        studyDate: readValue(item, "00080020") ?? "-",
        description: readValue(item, "00081030") ?? "No description",
        seriesCount: Number(readValue(item, "00201206") ?? 0),
        instanceCount: Number(readValue(item, "00201208") ?? 0),
    };
}
export default function PacsPage() {
    const [studies, setStudies] = useState([]);
    const [selectedUid, setSelectedUid] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/pacs/studies")
            .then((res) => {
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
            .then((data) => {
            const mapped = Array.isArray(data) ? data.map(mapStudy) : [];
            setStudies(mapped);
            if (mapped.length > 0) {
                setSelectedUid(mapped[0].studyInstanceUID);
            }
        })
            .catch((err) => {
            console.error(err);
            setError("Failed to load PACS studies from Orthanc");
        })
            .finally(() => setLoading(false));
    }, []);
    const selected = useMemo(() => studies.find((s) => s.studyInstanceUID === selectedUid), [studies, selectedUid]);
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "28px", marginBottom: "8px" }, children: "PACS" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Real Orthanc studies via backend PACS proxy" }), loading && _jsx("div", { children: "Loading studies..." }), error && _jsx("div", { style: { color: "#fca5a5" }, children: error }), !loading && !error && (_jsxs(_Fragment, { children: [_jsx("div", { style: {
                            overflowX: "auto",
                            border: "1px solid #374151",
                            borderRadius: "12px",
                            marginBottom: "20px",
                        }, children: _jsxs("table", { style: { width: "100%", borderCollapse: "collapse" }, children: [_jsx("thead", { style: { background: "#111827" }, children: _jsxs("tr", { children: [_jsx("th", { style: th, children: "Patient" }), _jsx("th", { style: th, children: "Patient ID" }), _jsx("th", { style: th, children: "Modality" }), _jsx("th", { style: th, children: "Date" }), _jsx("th", { style: th, children: "Series" }), _jsx("th", { style: th, children: "Instances" }), _jsx("th", { style: th, children: "Action" })] }) }), _jsxs("tbody", { children: [studies.map((study) => (_jsxs("tr", { children: [_jsx("td", { style: td, children: study.patientName }), _jsx("td", { style: td, children: study.patientId }), _jsx("td", { style: td, children: study.modality }), _jsx("td", { style: td, children: study.studyDate }), _jsx("td", { style: td, children: study.seriesCount }), _jsx("td", { style: td, children: study.instanceCount }), _jsx("td", { style: td, children: _jsx("button", { onClick: () => setSelectedUid(study.studyInstanceUID), style: {
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
                        }, children: [_jsx("div", { style: { fontSize: "20px", fontWeight: 700, marginBottom: "10px" }, children: "Selected Study" }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Patient:" }), " ", selected.patientName] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Patient ID:" }), " ", selected.patientId] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Modality:" }), " ", selected.modality] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Date:" }), " ", selected.studyDate] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Series:" }), " ", selected.seriesCount] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Instances:" }), " ", selected.instanceCount] }), _jsxs("div", { style: { marginBottom: "8px" }, children: [_jsx("strong", { children: "Study UID:" }), " ", selected.studyInstanceUID] }), _jsx("div", { style: { marginTop: "20px" }, children: _jsx("button", { onClick: () => window.open(`http://localhost:3005/viewer?StudyInstanceUIDs=${encodeURIComponent(selected.studyInstanceUID)}`, "_blank"), style: {
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
