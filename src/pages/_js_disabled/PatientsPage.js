import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiGet } from "@/lib/api";
import { createDoctorAssignment } from "@/lib/doctorAssignments";
export default function PatientsPage() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const doctorId = searchParams.get("doctorId") ?? "";
    const doctorName = searchParams.get("doctorName") ?? "";
    const [patients, setPatients] = useState([]);
    const [q, setQ] = useState("");
    const [department, setDepartment] = useState("all");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selectedId, setSelectedId] = useState("");
    const [assigning, setAssigning] = useState(false);
    const [marCount, setMarCount] = useState(0);
    useEffect(() => {
        async function loadPatients() {
            try {
                setLoading(true);
                setError("");
                const data = await apiGet("/patients");
                setPatients(Array.isArray(data) ? data : []);
            }
            catch (err) {
                console.error("ERROR:", err);
                setError("Failed to load patients");
                setPatients([]);
            }
            finally {
                setLoading(false);
            }
        }
        loadPatients();
    }, []);
    const filtered = useMemo(() => {
        const query = q.trim().toLowerCase();
        return patients.filter((p) => {
            const matchesText = !query ||
                p.id.toLowerCase().includes(query) ||
                p.name.toLowerCase().includes(query) ||
                String(p.department ?? "").toLowerCase().includes(query) ||
                String(p.condition ?? "").toLowerCase().includes(query);
            const matchesDepartment = department === "all" ||
                String(p.department ?? "").toLowerCase() === department.toLowerCase();
            return matchesText && matchesDepartment;
        });
    }, [patients, q, department]);
    const selected = patients.find((p) => p.id === selectedId) ||
        filtered[0] ||
        null;
    const handleAssignPatient = async () => {
        if (!selected || !doctorName || !doctorId)
            return;
        try {
            setAssigning(true);
            await createDoctorAssignment(doctorId, {
                patientId: selected.id,
                patientName: selected.name,
                department: selected.department,
                condition: selected.condition,
                status: "Assigned",
            });
            alert(`Patient ${selected.name} assigned to ${doctorName}`);
            navigate(`/doctors/${doctorId}`);
        }
        catch (err) {
            console.error(err);
            alert("Failed to assign patient");
        }
        finally {
            setAssigning(false);
        }
    };
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Patients System" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Electronic Medical Record workspace" }), doctorName && (_jsxs("div", { style: {
                    background: "#0f172a",
                    border: "1px solid #0f766e",
                    color: "#ccfbf1",
                    borderRadius: "14px",
                    padding: "14px 16px",
                    marginBottom: "18px",
                }, children: [_jsxs("div", { style: { fontWeight: 800, marginBottom: 4 }, children: ["Assign patient workflow for ", doctorName] }), _jsxs("div", { style: { opacity: 0.85, fontSize: 14 }, children: ["Doctor ID: ", doctorId || "N/A", " \u2022 Select a patient, then assign from the summary panel."] })] })), _jsxs("div", { style: { marginBottom: "16px", opacity: 0.8 }, children: ["Total patients: ", patients.length, " | Filtered: ", filtered.length] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "380px minmax(0,1fr)",
                    gap: "20px",
                    alignItems: "start",
                }, children: [_jsxs("div", { style: {
                            background: "#111827",
                            border: "1px solid #374151",
                            borderRadius: "16px",
                            padding: "16px",
                        }, children: [_jsxs("div", { style: { display: "grid", gap: "12px", marginBottom: "16px" }, children: [_jsx("input", { value: q, onChange: (e) => setQ(e.target.value), placeholder: "Search by ID, name, department, condition", style: {
                                            width: "100%",
                                            padding: "12px",
                                            borderRadius: "10px",
                                            border: "1px solid #4b5563",
                                            background: "#0f172a",
                                            color: "white",
                                        } }), _jsxs("select", { value: department, onChange: (e) => setDepartment(e.target.value), style: {
                                            width: "100%",
                                            padding: "12px",
                                            borderRadius: "10px",
                                            border: "1px solid #4b5563",
                                            background: "#0f172a",
                                            color: "white",
                                        }, children: [_jsx("option", { value: "all", children: "All departments" }), _jsx("option", { value: "cardiology", children: "Cardiology" }), _jsx("option", { value: "neurology", children: "Neurology" }), _jsx("option", { value: "orthopedics", children: "Orthopedics" }), _jsx("option", { value: "icu", children: "ICU" }), _jsx("option", { value: "emergency", children: "Emergency" })] })] }), loading && _jsx("p", { children: "Loading patients..." }), error && _jsx("p", { style: { color: "#fca5a5" }, children: error }), !loading && !error && filtered.length === 0 && (_jsx("p", { children: "No patients found." })), !loading && !error && filtered.length > 0 && (_jsx("div", { style: { display: "grid", gap: "10px" }, children: filtered.map((p) => {
                                    const active = selected?.id === p.id;
                                    return (_jsxs("button", { onClick: () => setSelectedId(p.id), style: {
                                            textAlign: "left",
                                            padding: "14px",
                                            borderRadius: "12px",
                                            border: active ? "1px solid #60a5fa" : "1px solid #374151",
                                            background: active ? "#1e3a8a" : "#0f172a",
                                            color: "white",
                                            cursor: "pointer",
                                        }, children: [_jsx("div", { style: { fontWeight: 700 }, children: p.name }), _jsxs("div", { style: { fontSize: "13px", opacity: 0.8 }, children: ["ID: ", p.id] }), _jsxs("div", { style: { fontSize: "13px", opacity: 0.8 }, children: [p.department ?? "No department", " \u2022 ", p.condition ?? "No condition"] })] }, p.id));
                                }) }))] }), _jsxs("div", { style: {
                            background: "#111827",
                            border: "1px solid #374151",
                            borderRadius: "16px",
                            padding: "20px",
                            minHeight: "500px",
                        }, children: [_jsx("h2", { style: { marginTop: 0, marginBottom: "16px" }, children: "Patient Summary" }), !selected ? (_jsx("p", { children: "Select a patient to view details." })) : (_jsxs("div", { style: { display: "grid", gap: "12px" }, children: [_jsxs("div", { children: [_jsx("strong", { children: "Name:" }), " ", selected.name] }), _jsxs("div", { children: [_jsx("strong", { children: "ID:" }), " ", selected.id] }), _jsxs("div", { children: [_jsx("strong", { children: "Age:" }), " ", selected.age ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Gender:" }), " ", selected.gender ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Phone:" }), " ", selected.phone ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Department:" }), " ", selected.department ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Condition:" }), " ", selected.condition ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "Status:" }), " ", selected.status ?? "—"] }), _jsxs("div", { children: [_jsx("strong", { children: "MAR Count:" }), " ", marCount] }), _jsxs("div", { style: {
                                            marginTop: "16px",
                                            display: "flex",
                                            gap: "12px",
                                            flexWrap: "wrap",
                                        }, children: [_jsx("button", { onClick: () => navigate(`/patient-profile?id=${selected.id}`), style: {
                                                    padding: "12px 16px",
                                                    borderRadius: "10px",
                                                    border: "none",
                                                    background: "#2563eb",
                                                    color: "white",
                                                    cursor: "pointer",
                                                    fontWeight: 600,
                                                }, children: "Open Patient Profile" }), _jsx("button", { onClick: () => navigate(`/nurses?patientId=${selected.id}`), style: {
                                                    padding: "12px 16px",
                                                    borderRadius: "10px",
                                                    border: "none",
                                                    background: "#7c3aed",
                                                    color: "white",
                                                    cursor: "pointer",
                                                    fontWeight: 600,
                                                }, children: "Open Nursing Station" }), doctorName && (_jsx("button", { onClick: handleAssignPatient, disabled: assigning, style: {
                                                    padding: "12px 16px",
                                                    borderRadius: "10px",
                                                    border: "none",
                                                    background: "#0f766e",
                                                    color: "white",
                                                    cursor: assigning ? "not-allowed" : "pointer",
                                                    opacity: assigning ? 0.7 : 1,
                                                    fontWeight: 700,
                                                }, children: assigning ? "Assigning..." : "Assign Selected Patient" }))] })] }))] })] })] }));
}
