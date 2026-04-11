import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
export default function NotesPage() {
    const [patientId, setPatientId] = useState("P-1001");
    const [notes, setNotes] = useState([]);
    const [text, setText] = useState("");
    useEffect(() => {
        if (!patientId)
            return;
        apiGet(`/notes/${patientId}`)
            .then((data) => setNotes(Array.isArray(data) ? data : []))
            .catch(() => setNotes([]));
    }, [patientId]);
    async function add() {
        if (!text.trim())
            return;
        await apiPost(`/notes/${patientId}`, { text });
        const data = await apiGet(`/notes/${patientId}`);
        setNotes(Array.isArray(data) ? data : []);
        setText("");
    }
    return (_jsxs("div", { style: { padding: 24, color: "white" }, children: [_jsx("h1", { style: { fontSize: 32, fontWeight: 700, marginBottom: 8 }, children: "Clinical Notes" }), _jsx("p", { style: { opacity: 0.7, marginBottom: 20 }, children: "Create and view notes for the selected patient." }), _jsxs("div", { style: { background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: 20, maxWidth: 700 }, children: [_jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("div", { style: { marginBottom: 6 }, children: "Patient ID" }), _jsx("input", { value: patientId, onChange: (e) => setPatientId(e.target.value), style: inputStyle })] }), _jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("div", { style: { marginBottom: 6 }, children: "New Note" }), _jsx("textarea", { value: text, onChange: (e) => setText(e.target.value), placeholder: "Write clinical note...", style: textareaStyle })] }), _jsx("button", { onClick: add, style: buttonStyle, children: "Add Note" })] }), _jsxs("div", { style: { marginTop: 20, background: "#111827", border: "1px solid #374151", borderRadius: 12, padding: 20, maxWidth: 700 }, children: [_jsx("h2", { style: { fontSize: 24, fontWeight: 700, marginBottom: 12 }, children: "Patient Notes" }), notes.length === 0 ? (_jsx("div", { style: { opacity: 0.7 }, children: "No notes for this patient." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: notes.map((note) => (_jsx("div", { style: {
                                background: "#0b1220",
                                border: "1px solid #374151",
                                borderRadius: 10,
                                padding: 12,
                            }, children: note.text }, note.id))) }))] })] }));
}
const inputStyle = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 10,
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const textareaStyle = {
    width: "100%",
    minHeight: 120,
    padding: "12px",
    borderRadius: 10,
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const buttonStyle = {
    padding: "12px 18px",
    borderRadius: 10,
    border: "1px solid #22c55e",
    background: "#166534",
    color: "white",
    cursor: "pointer",
    fontWeight: 600,
};
