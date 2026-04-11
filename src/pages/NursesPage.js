import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiDelete, apiGet, apiPost, apiPut } from "@/lib/api";
export default function NursesPage() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const patientIdFromUrl = searchParams.get("patientId") ?? "";
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState(patientIdFromUrl);
    const [vitals, setVitals] = useState([]);
    const [notes, setNotes] = useState([]);
    const [mar, setMar] = useState([]);
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [marFilter, setMarFilter] = useState("all");
    const [marSearch, setMarSearch] = useState("");
    const [editingMarId, setEditingMarId] = useState(null);
    const [vitalForm, setVitalForm] = useState({
        temperature: "",
        bloodPressure: "",
        heartRate: "",
        respiratoryRate: "",
        oxygenSaturation: "",
        time: "",
    });
    const [noteForm, setNoteForm] = useState({
        text: "",
    });
    const [marForm, setMarForm] = useState({
        medication: "",
        dose: "",
        route: "",
        schedule: "",
        status: "Pending",
        givenAt: "",
    });
    useEffect(() => {
        if (!successMessage)
            return;
        const t = setTimeout(() => setSuccessMessage(""), 2500);
        return () => clearTimeout(t);
    }, [successMessage]);
    useEffect(() => {
        apiGet("/patients")
            .then((data) => {
            const list = Array.isArray(data) ? data : [];
            setPatients(list);
            if (patientIdFromUrl) {
                setSelectedPatientId(patientIdFromUrl);
            }
            else if (list.length > 0) {
                setSelectedPatientId(list[0].id);
                setSearchParams({ patientId: list[0].id });
            }
        })
            .catch(() => setError("Failed to load patients"));
    }, []);
    useEffect(() => {
        if (!selectedPatientId)
            return;
        setSearchParams({ patientId: selectedPatientId });
        Promise.all([
            apiGet(`/nursing/vitals/${selectedPatientId}`),
            apiGet(`/nursing/notes/${selectedPatientId}`),
            apiGet(`/mar/${selectedPatientId}`),
        ])
            .then(([v, n, m]) => {
            setVitals(Array.isArray(v) ? v : []);
            setNotes(Array.isArray(n) ? n : []);
            setMar(Array.isArray(m) ? m : []);
        })
            .catch(() => setError("Failed to load nursing data"));
    }, [selectedPatientId]);
    const selectedPatient = useMemo(() => patients.find((p) => p.id === selectedPatientId), [patients, selectedPatientId]);
    const filteredMar = useMemo(() => {
        let items = [...mar];
        items.sort((a, b) => {
            const rank = (status) => {
                if (status === "Pending")
                    return 0;
                if (status === "Given")
                    return 1;
                return 2;
            };
            return rank(a.status) - rank(b.status);
        });
        if (marFilter !== "all") {
            items = items.filter((item) => item.status === marFilter);
        }
        const q = marSearch.trim().toLowerCase();
        if (q) {
            items = items.filter((item) => item.medication.toLowerCase().includes(q));
        }
        return items;
    }, [mar, marFilter, marSearch]);
    const totalMarCount = mar.length;
    const pendingMarCount = mar.filter((item) => item.status === "Pending").length;
    const givenMarCount = mar.filter((item) => item.status === "Given").length;
    const resetMarForm = () => {
        setMarForm({
            medication: "",
            dose: "",
            route: "",
            schedule: "",
            status: "Pending",
            givenAt: "",
        });
        setEditingMarId(null);
    };
    const submitVital = async (e) => {
        e.preventDefault();
        try {
            await apiPost(`/nursing/vitals/${selectedPatientId}`, vitalForm);
            const refreshed = await apiGet(`/nursing/vitals/${selectedPatientId}`);
            setVitals(Array.isArray(refreshed) ? refreshed : []);
            setVitalForm({
                temperature: "",
                bloodPressure: "",
                heartRate: "",
                respiratoryRate: "",
                oxygenSaturation: "",
                time: "",
            });
            setSuccessMessage("Vital signs saved");
        }
        catch {
            setError("Failed to save vital signs");
        }
    };
    const submitNote = async (e) => {
        e.preventDefault();
        try {
            await apiPost(`/nursing/notes/${selectedPatientId}`, noteForm);
            const refreshed = await apiGet(`/nursing/notes/${selectedPatientId}`);
            setNotes(Array.isArray(refreshed) ? refreshed : []);
            setNoteForm({ text: "" });
            setSuccessMessage("Note saved");
        }
        catch {
            setError("Failed to save nursing note");
        }
    };
    const submitMAR = async (e) => {
        e.preventDefault();
        try {
            if (editingMarId !== null) {
                await apiPut(`/mar/${selectedPatientId}/${editingMarId}`, marForm);
            }
            else {
                await apiPost(`/mar/${selectedPatientId}`, marForm);
            }
            const refreshed = await apiGet(`/mar/${selectedPatientId}`);
            setMar(Array.isArray(refreshed) ? refreshed : []);
            resetMarForm();
            setSuccessMessage(editingMarId !== null ? "MAR updated" : "MAR added");
        }
        catch {
            setError("Failed to save MAR item");
        }
    };
    const markAsGiven = async (itemId) => {
        try {
            const now = new Date();
            const hh = String(now.getHours()).padStart(2, "0");
            const mm = String(now.getMinutes()).padStart(2, "0");
            await apiPut(`/mar/${selectedPatientId}/${itemId}/status`, {
                status: "Given",
                givenAt: `${hh}:${mm}`,
            });
            const refreshed = await apiGet(`/mar/${selectedPatientId}`);
            setMar(Array.isArray(refreshed) ? refreshed : []);
            setSuccessMessage("Medication marked as given");
        }
        catch {
            setError("Failed to update MAR status");
        }
    };
    const markAllPendingAsGiven = async () => {
        try {
            const pending = mar.filter((item) => item.status === "Pending");
            if (pending.length === 0)
                return;
            const now = new Date();
            const hh = String(now.getHours()).padStart(2, "0");
            const mm = String(now.getMinutes()).padStart(2, "0");
            const givenAt = `${hh}:${mm}`;
            await Promise.all(pending.map((item) => apiPut(`/mar/${selectedPatientId}/${item.id}/status`, {
                status: "Given",
                givenAt,
            })));
            const refreshed = await apiGet(`/mar/${selectedPatientId}`);
            setMar(Array.isArray(refreshed) ? refreshed : []);
            setMarFilter("Given");
            setSuccessMessage("All pending meds marked as given");
        }
        catch {
            setError("Failed to update MAR");
        }
    };
    const startEditMarItem = (item) => {
        setEditingMarId(item.id);
        setMarForm({
            medication: item.medication,
            dose: item.dose,
            route: item.route,
            schedule: item.schedule,
            status: item.status,
            givenAt: item.givenAt || "",
        });
    };
    const deleteMarItem = async (itemId) => {
        const ok = window.confirm("Delete this MAR item?");
        if (!ok)
            return;
        try {
            await apiDelete(`/mar/${selectedPatientId}/${itemId}`);
            const refreshed = await apiGet(`/mar/${selectedPatientId}`);
            setMar(Array.isArray(refreshed) ? refreshed : []);
            setSuccessMessage("MAR item deleted");
        }
        catch {
            setError("Failed to delete MAR item");
        }
    };
    return (_jsx("div", { style: {
            minHeight: "100vh",
            background: "linear-gradient(180deg, #0f172a 0%, #111827 100%)",
            color: "#f8fafc",
            padding: 24,
        }, children: _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }, children: [_jsxs("div", { children: [_jsx("h1", { style: { margin: 0, fontSize: 42, fontWeight: 800 }, children: "Nursing Station \u2022 NEW UI" }), _jsx("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: "SMART NURSING WORKFLOW \u2022 GLASS VERSION ACTIVE" })] }), selectedPatientId && (_jsx("button", { onClick: () => navigate(`/patient-profile?id=${selectedPatientId}`), style: {
                                border: "1px solid rgba(148,163,184,0.35)",
                                borderRadius: 14,
                                padding: "12px 16px",
                                background: "rgba(255,255,255,0.08)",
                                color: "#e5e7eb",
                                fontWeight: 700,
                                cursor: "pointer",
                            }, children: "Open Patient Profile" }))] }), error && (_jsx("div", { style: {
                        background: "linear-gradient(180deg, rgba(127,29,29,0.5), rgba(69,10,10,0.55))",
                        border: "1px solid rgba(248,113,113,0.45)",
                        color: "#fecaca",
                        borderRadius: 20,
                        padding: 16,
                    }, children: error })), successMessage && (_jsx("div", { style: {
                        background: "linear-gradient(180deg, rgba(20,83,45,0.5), rgba(5,46,22,0.55))",
                        border: "1px solid rgba(74,222,128,0.45)",
                        color: "#bbf7d0",
                        borderRadius: 20,
                        padding: 16,
                    }, children: successMessage })), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1.1fr 2fr", gap: 20 }, children: [_jsxs("div", { style: {
                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                border: "1px solid rgba(96,165,250,0.28)",
                                borderRadius: 24,
                                padding: 22,
                                boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
                            }, children: [_jsx("h2", { style: { marginTop: 0, marginBottom: 16, fontSize: 28 }, children: "Patients" }), _jsx("div", { style: { display: "grid", gap: 14 }, children: patients.map((patient) => (_jsxs("button", { onClick: () => setSelectedPatientId(patient.id), style: {
                                            textAlign: "left",
                                            padding: 16,
                                            borderRadius: 18,
                                            border: selectedPatientId === patient.id
                                                ? "1px solid rgba(56,189,248,0.95)"
                                                : "1px solid rgba(148,163,184,0.22)",
                                            background: selectedPatientId === patient.id
                                                ? "linear-gradient(135deg, rgba(37,99,235,0.34), rgba(14,165,233,0.18))"
                                                : "linear-gradient(180deg, rgba(15,23,42,0.55), rgba(30,41,59,0.55))",
                                            boxShadow: selectedPatientId === patient.id
                                                ? "0 0 0 1px rgba(59,130,246,0.18), 0 10px 24px rgba(2,132,199,0.18)"
                                                : "0 8px 18px rgba(15,23,42,0.16)",
                                            color: "#f8fafc",
                                            cursor: "pointer",
                                        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: patient.name }), _jsx("div", { style: { marginTop: 6, color: "#cbd5e1" }, children: patient.id }), _jsxs("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: [patient.department ?? "General", " \u2022 ", patient.condition ?? "-"] })] }, patient.id))) })] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { style: {
                                        background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                        border: "1px solid rgba(96,165,250,0.28)",
                                        borderRadius: 24,
                                        padding: 22,
                                        boxShadow: "0 10px 30px rgba(0,0,0,0.25)",
                                    }, children: [_jsx("h2", { style: { marginTop: 0, marginBottom: 16, fontSize: 28 }, children: "Selected Patient" }), selectedPatient ? (_jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Name:" }), " ", selectedPatient.name] }), _jsxs("div", { children: [_jsx("strong", { children: "ID:" }), " ", selectedPatient.id] }), _jsxs("div", { children: [_jsx("strong", { children: "Age:" }), " ", selectedPatient.age ?? "-"] }), _jsxs("div", { children: [_jsx("strong", { children: "Gender:" }), " ", selectedPatient.gender ?? "-"] }), _jsxs("div", { children: [_jsx("strong", { children: "Department:" }), " ", selectedPatient.department ?? "-"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", selectedPatient.status ?? "-"] }), _jsxs("div", { style: { gridColumn: "1 / -1" }, children: [_jsx("strong", { children: "Condition:" }), " ", selectedPatient.condition ?? "-"] })] })) : (_jsx("div", { children: "No patient selected" }))] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }, children: [_jsxs("form", { onSubmit: submitVital, style: {
                                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                                border: "1px solid rgba(96,165,250,0.28)",
                                                borderRadius: 24,
                                                padding: 22,
                                            }, children: [_jsx("h3", { style: { marginTop: 0, marginBottom: 14, fontSize: 24 }, children: "Add Vitals" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }, children: [_jsx("input", { style: inputStyle, placeholder: "Temp", value: vitalForm.temperature, onChange: (e) => setVitalForm({ ...vitalForm, temperature: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "BP", value: vitalForm.bloodPressure, onChange: (e) => setVitalForm({ ...vitalForm, bloodPressure: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "HR", value: vitalForm.heartRate, onChange: (e) => setVitalForm({ ...vitalForm, heartRate: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "RR", value: vitalForm.respiratoryRate, onChange: (e) => setVitalForm({ ...vitalForm, respiratoryRate: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "SpO2", value: vitalForm.oxygenSaturation, onChange: (e) => setVitalForm({ ...vitalForm, oxygenSaturation: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "Time", value: vitalForm.time, onChange: (e) => setVitalForm({ ...vitalForm, time: e.target.value }) })] }), _jsx("div", { style: { marginTop: 14 }, children: _jsx("button", { type: "submit", style: primaryBtn, children: "Save Vitals" }) })] }), _jsxs("form", { onSubmit: submitNote, style: {
                                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                                border: "1px solid rgba(96,165,250,0.28)",
                                                borderRadius: 24,
                                                padding: 22,
                                            }, children: [_jsx("h3", { style: { marginTop: 0, marginBottom: 14, fontSize: 24 }, children: "Add Note" }), _jsx("textarea", { style: { ...inputStyle, minHeight: 132, resize: "vertical" }, placeholder: "Write nursing note...", value: noteForm.text, onChange: (e) => setNoteForm({ text: e.target.value }) }), _jsx("div", { style: { marginTop: 14 }, children: _jsx("button", { type: "submit", style: primaryBtn, children: "Save Note" }) })] })] }), _jsxs("form", { onSubmit: submitMAR, style: {
                                        background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                        border: "1px solid rgba(96,165,250,0.28)",
                                        borderRadius: 24,
                                        padding: 22,
                                    }, children: [_jsx("h3", { style: { marginTop: 0, marginBottom: 14, fontSize: 24 }, children: editingMarId !== null ? "Edit Medication Administration Record (MAR)" : "Medication Administration Record (MAR)" }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "2fr 1fr 1fr 1.4fr", gap: 10 }, children: [_jsx("input", { style: inputStyle, placeholder: "Medication", value: marForm.medication, onChange: (e) => setMarForm({ ...marForm, medication: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "Dose", value: marForm.dose, onChange: (e) => setMarForm({ ...marForm, dose: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "Route", value: marForm.route, onChange: (e) => setMarForm({ ...marForm, route: e.target.value }) }), _jsx("input", { style: inputStyle, placeholder: "Schedule", value: marForm.schedule, onChange: (e) => setMarForm({ ...marForm, schedule: e.target.value }) })] }), _jsxs("div", { style: { display: "flex", gap: 10, marginTop: 14, flexWrap: "wrap" }, children: [_jsx("button", { type: "submit", style: primaryBtn, children: editingMarId !== null ? "Update MAR" : "Add MAR" }), editingMarId !== null && (_jsx("button", { type: "button", style: secondaryBtn, onClick: resetMarForm, children: "Cancel Edit" }))] })] }), _jsxs("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1.3fr", gap: 20 }, children: [_jsxs("div", { style: {
                                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                                border: "1px solid rgba(96,165,250,0.28)",
                                                borderRadius: 24,
                                                padding: 22,
                                            }, children: [_jsx("h3", { style: { marginTop: 0, marginBottom: 14, fontSize: 24 }, children: "Vital History" }), _jsx("div", { style: { display: "grid", gap: 12 }, children: vitals.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No vitals yet" })) : vitals.map((item) => (_jsxs("div", { style: itemStyle, children: [_jsxs("div", { children: [_jsx("strong", { children: "Temp:" }), " ", item.temperature, " \u00B0C"] }), _jsxs("div", { children: [_jsx("strong", { children: "BP:" }), " ", item.bloodPressure] }), _jsxs("div", { children: [_jsx("strong", { children: "HR:" }), " ", item.heartRate] }), _jsxs("div", { children: [_jsx("strong", { children: "RR:" }), " ", item.respiratoryRate] }), _jsxs("div", { children: [_jsx("strong", { children: "SpO2:" }), " ", item.oxygenSaturation, "%"] }), _jsx("div", { style: { marginTop: 8, color: "#cbd5e1" }, children: item.time })] }, item.id))) })] }), _jsxs("div", { style: {
                                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                                border: "1px solid rgba(96,165,250,0.28)",
                                                borderRadius: 24,
                                                padding: 22,
                                            }, children: [_jsx("h3", { style: { marginTop: 0, marginBottom: 14, fontSize: 24 }, children: "Nursing Notes" }), _jsx("div", { style: { display: "grid", gap: 12 }, children: notes.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No notes yet" })) : notes.map((item) => (_jsx("div", { style: itemStyle, children: item.text }, item.id))) })] }), _jsxs("div", { style: {
                                                background: "linear-gradient(180deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92))",
                                                border: "1px solid rgba(96,165,250,0.28)",
                                                borderRadius: 24,
                                                padding: 22,
                                            }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "center" }, children: [_jsx("h3", { style: { margin: 0, fontSize: 24 }, children: "MAR List" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: markAllPendingAsGiven, children: "Mark all Pending as Given" })] }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap", marginTop: 14 }, children: [_jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Total:" }), " ", totalMarCount] }), _jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Pending:" }), " ", pendingMarCount] }), _jsxs("div", { style: itemStyle, children: [_jsx("strong", { children: "Given:" }), " ", givenMarCount] })] }), _jsxs("div", { style: { display: "flex", gap: 8, marginTop: 14, flexWrap: "wrap" }, children: [_jsx("button", { type: "button", style: secondaryBtn, onClick: () => setMarFilter("all"), children: "All" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => setMarFilter("Pending"), children: "Pending" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => setMarFilter("Given"), children: "Given" })] }), _jsxs("div", { style: { display: "flex", gap: 8, marginTop: 14 }, children: [_jsx("input", { style: inputStyle, placeholder: "Search medication name...", value: marSearch, onChange: (e) => setMarSearch(e.target.value) }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => setMarSearch(""), children: "Clear" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => {
                                                                setMarSearch("");
                                                                setMarFilter("all");
                                                            }, children: "Reset" })] }), _jsx("div", { style: { display: "grid", gap: 12, marginTop: 16 }, children: filteredMar.length === 0 ? (_jsx("div", { style: { color: "#cbd5e1" }, children: "No MAR items for this filter or search." })) : filteredMar.map((m) => (_jsxs("div", { style: itemStyle, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: m.medication }), _jsxs("div", { style: { marginTop: 6, color: "#e2e8f0" }, children: [m.dose, " \u2022 ", m.route, " \u2022 ", m.schedule] }), _jsxs("div", { style: {
                                                                    display: "inline-block",
                                                                    marginTop: 10,
                                                                    padding: "6px 10px",
                                                                    borderRadius: 999,
                                                                    fontSize: 13,
                                                                    fontWeight: 800,
                                                                    background: m.status === "Given" ? "#dcfce7" : "#fef3c7",
                                                                    color: m.status === "Given" ? "#166534" : "#92400e",
                                                                }, children: [m.status, m.givenAt ? ` at ${m.givenAt}` : ""] }), m.createdAt && (_jsxs("div", { style: { marginTop: 8, color: "#cbd5e1", fontSize: 13 }, children: ["Created: ", m.createdAt] })), _jsxs("div", { style: { display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12 }, children: [m.status !== "Given" && (_jsx("button", { type: "button", style: primaryBtn, onClick: () => markAsGiven(m.id), children: "Mark as Given" })), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => startEditMarItem(m), children: "Edit" }), _jsx("button", { type: "button", style: secondaryBtn, onClick: () => deleteMarItem(m.id), children: "Delete" })] })] }, m.id))) })] })] })] })] })] }) }));
}
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
    padding: "12px 16px",
    background: "linear-gradient(135deg, #0ea5e9, #2563eb)",
    color: "white",
    fontWeight: 700,
    cursor: "pointer",
};
const secondaryBtn = {
    border: "1px solid rgba(148,163,184,0.35)",
    borderRadius: 14,
    padding: "12px 16px",
    background: "rgba(255,255,255,0.08)",
    color: "#e5e7eb",
    fontWeight: 700,
    cursor: "pointer",
};
const itemStyle = {
    background: "linear-gradient(180deg, rgba(37,99,235,0.18), rgba(15,23,42,0.30))",
    border: "1px solid rgba(96,165,250,0.26)",
    borderRadius: 18,
    padding: 16,
    boxShadow: "0 8px 18px rgba(0,0,0,0.18)",
};
