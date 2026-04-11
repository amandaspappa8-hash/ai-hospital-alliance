import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getDoctorById } from "@/lib/doctors";
import { getDoctorAssignments, removeDoctorAssignment, updateDoctorAssignmentStatus, } from "@/lib/doctorAssignments";
import { createAppointment, getAppointments, } from "@/lib/appointments";
import { addDoctorNote, getDoctorNotes, removeDoctorNote, } from "@/lib/doctorNotes";
function exportDoctorSummaryPDF() {
    const element = document.getElementById("doctor-summary-report");
    if (!element) {
        alert("Doctor summary not found");
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
        <title>Doctor Summary Report</title>
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
}
function statusColor(status) {
    if (status === "Available")
        return { bg: "#dcfce7", color: "#166534" };
    if (status === "On Call")
        return { bg: "#fef3c7", color: "#92400e" };
    if (status === "In Surgery")
        return { bg: "#fee2e2", color: "#991b1b" };
    return { bg: "#e5e7eb", color: "#374151" };
}
function assignmentTone(status) {
    const value = String(status ?? "").toLowerCase();
    if (value === "completed")
        return { bg: "#dcfce7", color: "#166534" };
    if (value === "in follow-up")
        return { bg: "#fef3c7", color: "#92400e" };
    return { bg: "#dbeafe", color: "#1d4ed8" };
}
function appointmentTone(status) {
    const value = String(status ?? "").toLowerCase();
    if (value.includes("scheduled"))
        return { bg: "#dbeafe", color: "#1d4ed8" };
    if (value.includes("waiting"))
        return { bg: "#fef3c7", color: "#92400e" };
    if (value.includes("completed"))
        return { bg: "#dcfce7", color: "#166534" };
    return { bg: "#e5e7eb", color: "#374151" };
}
export default function DoctorProfilePage() {
    const { doctorId = "" } = useParams();
    const navigate = useNavigate();
    const [doctor, setDoctor] = useState(null);
    const [assignments, setAssignments] = useState([]);
    const [appointments, setAppointments] = useState([]);
    const [doctorNotes, setDoctorNotes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [busyId, setBusyId] = useState(null);
    const [showCreateAppointment, setShowCreateAppointment] = useState(false);
    const [creatingAppointment, setCreatingAppointment] = useState(false);
    const [appointmentPatient, setAppointmentPatient] = useState("");
    const [appointmentDepartment, setAppointmentDepartment] = useState("");
    const [appointmentTime, setAppointmentTime] = useState("");
    const [showQuickNote, setShowQuickNote] = useState(false);
    const [quickNoteText, setQuickNoteText] = useState("");
    async function loadDoctorProfile() {
        if (!doctorId)
            return;
        try {
            setLoading(true);
            setError("");
            const doctorData = await getDoctorById(doctorId);
            const [assignmentsData, appointmentsData] = await Promise.all([
                getDoctorAssignments(doctorId),
                getAppointments(),
            ]);
            const doctorAppointments = Array.isArray(appointmentsData)
                ? appointmentsData.filter((item) => item.doctor.toLowerCase().includes(doctorData.name.toLowerCase()))
                : [];
            setDoctor(doctorData);
            setAssignments(assignmentsData);
            setAppointments(doctorAppointments);
            setDoctorNotes(getDoctorNotes(doctorId));
            setAppointmentDepartment(doctorData.specialty || doctorData.department || "");
        }
        catch (err) {
            console.error(err);
            setError("Failed to load doctor profile");
            setDoctor(null);
            setAssignments([]);
            setAppointments([]);
            setDoctorNotes([]);
        }
        finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        loadDoctorProfile();
    }, [doctorId]);
    const badge = useMemo(() => doctor
        ? statusColor(doctor.status)
        : { bg: "#e5e7eb", color: "#374151" }, [doctor]);
    const assignmentStats = useMemo(() => {
        const assigned = assignments.filter((item) => String(item.status ?? "").toLowerCase() === "assigned").length;
        const followUp = assignments.filter((item) => String(item.status ?? "").toLowerCase() === "in follow-up").length;
        const completed = assignments.filter((item) => String(item.status ?? "").toLowerCase() === "completed").length;
        return {
            total: assignments.length,
            assigned,
            followUp,
            completed,
        };
    }, [assignments]);
    const handleStatusChange = async (assignmentId, status) => {
        if (!doctorId)
            return;
        try {
            setBusyId(assignmentId);
            await updateDoctorAssignmentStatus(doctorId, assignmentId, status);
            setAssignments((current) => current.map((item) => item.id === assignmentId ? { ...item, status } : item));
        }
        catch (err) {
            console.error(err);
            alert("Failed to update assignment status");
        }
        finally {
            setBusyId(null);
        }
    };
    const handleRemove = async (assignmentId) => {
        if (!doctorId)
            return;
        try {
            setBusyId(assignmentId);
            await removeDoctorAssignment(doctorId, assignmentId);
            setAssignments((current) => current.filter((item) => item.id !== assignmentId));
        }
        catch (err) {
            console.error(err);
            alert("Failed to remove assignment");
        }
        finally {
            setBusyId(null);
        }
    };
    const handleCreateAppointment = async () => {
        if (!doctor)
            return;
        if (!appointmentPatient.trim() || !appointmentDepartment.trim() || !appointmentTime.trim()) {
            alert("Please fill patient name, department, and time");
            return;
        }
        try {
            setCreatingAppointment(true);
            const created = await createAppointment({
                patient: appointmentPatient.trim(),
                department: appointmentDepartment.trim(),
                doctor: doctor.name,
                time: appointmentTime.trim(),
                status: "Scheduled",
            });
            setAppointments((current) => [...current, created]);
            setAppointmentPatient("");
            setAppointmentTime("");
            setShowCreateAppointment(false);
        }
        catch (err) {
            console.error(err);
            alert("Failed to create appointment");
        }
        finally {
            setCreatingAppointment(false);
        }
    };
    const handleCreateQuickNote = () => {
        if (!doctorId)
            return;
        if (!quickNoteText.trim()) {
            alert("Please enter a note");
            return;
        }
        const created = addDoctorNote(doctorId, quickNoteText.trim());
        setDoctorNotes((current) => [created, ...current]);
        setQuickNoteText("");
        setShowQuickNote(false);
    };
    const handleRemoveNote = (noteId) => {
        if (!doctorId)
            return;
        removeDoctorNote(doctorId, noteId);
        setDoctorNotes((current) => current.filter((note) => note.id !== noteId));
    };
    return (_jsxs("div", { style: { padding: 24, color: "#e5eef8" }, children: [_jsxs("div", { style: { marginBottom: 20, display: "flex", gap: 12, flexWrap: "wrap" }, children: [_jsx("button", { onClick: () => navigate("/doctors"), style: {
                            padding: "10px 14px",
                            borderRadius: 12,
                            border: "1px solid #334155",
                            background: "#0f172a",
                            color: "white",
                            cursor: "pointer",
                            fontWeight: 700,
                        }, children: "\u2190 Back to Doctors" }), doctor?.specialty && (_jsxs("button", { onClick: () => navigate(`/specialties/${doctor.specialty.toLowerCase()}`), style: {
                            padding: "10px 14px",
                            borderRadius: 12,
                            border: "1px solid #334155",
                            background: "#1e293b",
                            color: "white",
                            cursor: "pointer",
                            fontWeight: 700,
                        }, children: ["Open ", doctor.specialty] })), _jsx("button", { onClick: exportDoctorSummaryPDF, style: {
                            padding: "10px 14px",
                            borderRadius: 12,
                            border: "none",
                            background: "#2563eb",
                            color: "white",
                            cursor: "pointer",
                            fontWeight: 800,
                        }, children: "Export Doctor Summary PDF" })] }), error && _jsx("div", { style: { color: "#fecaca", marginBottom: 16 }, children: error }), loading && _jsx("div", { style: { marginBottom: 16 }, children: "Loading doctor profile..." }), !loading && !doctor ? _jsx("div", { children: "Doctor not found." }) : null, doctor && (_jsxs("div", { id: "doctor-summary-report", style: {
                    display: "grid",
                    gridTemplateColumns: "1.2fr 1fr",
                    gap: 20,
                }, children: [_jsxs("div", { className: "avoid-break", style: {
                            background: "#f8fafc",
                            color: "#0f172a",
                            borderRadius: 26,
                            padding: 24,
                            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                        }, children: [_jsxs("div", { style: {
                                    display: "grid",
                                    gridTemplateColumns: "120px 1fr",
                                    gap: 20,
                                    alignItems: "center",
                                    marginBottom: 24,
                                }, children: [_jsx("div", { style: {
                                            width: 120,
                                            height: 120,
                                            borderRadius: 28,
                                            background: "#dbeafe",
                                            color: "#1d4ed8",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center",
                                            fontSize: 40,
                                            fontWeight: 800,
                                        }, children: doctor.name
                                            .split(" ")
                                            .slice(0, 2)
                                            .map((p) => p[0])
                                            .join("") }), _jsxs("div", { children: [_jsx("div", { style: { fontSize: 30, fontWeight: 800, marginBottom: 6 }, children: doctor.name }), _jsxs("div", { style: { color: "#475569", fontSize: 17, marginBottom: 8 }, children: [doctor.specialty, " \u2022 ", doctor.department] }), _jsx("div", { style: {
                                                    display: "inline-block",
                                                    background: badge.bg,
                                                    color: badge.color,
                                                    padding: "7px 12px",
                                                    borderRadius: 999,
                                                    fontWeight: 800,
                                                    fontSize: 13,
                                                }, children: doctor.status })] })] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "white",
                                    border: "1px solid #e2e8f0",
                                    borderRadius: 20,
                                    padding: 18,
                                    display: "grid",
                                    gap: 12,
                                    marginBottom: 18,
                                }, children: [_jsx(InfoRow, { label: "Doctor ID", value: doctor.id }), _jsx(InfoRow, { label: "Department", value: doctor.department }), _jsx(InfoRow, { label: "Specialty", value: doctor.specialty }), _jsx(InfoRow, { label: "Experience", value: doctor.experience }), _jsx(InfoRow, { label: "Schedule", value: doctor.schedule }), _jsx(InfoRow, { label: "Phone", value: doctor.phone })] }), _jsxs("div", { style: {
                                    display: "flex",
                                    gap: 12,
                                    flexWrap: "wrap",
                                }, children: [_jsx("button", { onClick: () => navigate(`/appointments?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`), style: {
                                            padding: "12px 16px",
                                            borderRadius: 14,
                                            border: "none",
                                            background: "#2563eb",
                                            color: "white",
                                            cursor: "pointer",
                                            fontWeight: 800,
                                        }, children: "Book Appointment" }), _jsx("button", { onClick: () => setShowCreateAppointment((v) => !v), style: {
                                            padding: "12px 16px",
                                            borderRadius: 14,
                                            border: "none",
                                            background: "#7c3aed",
                                            color: "white",
                                            cursor: "pointer",
                                            fontWeight: 800,
                                        }, children: "Create Appointment" }), _jsx("button", { onClick: () => setShowQuickNote((v) => !v), style: {
                                            padding: "12px 16px",
                                            borderRadius: 14,
                                            border: "none",
                                            background: "#0f766e",
                                            color: "white",
                                            cursor: "pointer",
                                            fontWeight: 800,
                                        }, children: "Create Quick Note" }), _jsx("button", { onClick: () => navigate(`/patients?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`), style: {
                                            padding: "12px 16px",
                                            borderRadius: 14,
                                            border: "none",
                                            background: "#ea580c",
                                            color: "white",
                                            cursor: "pointer",
                                            fontWeight: 800,
                                        }, children: "Assign Patient" })] }), showCreateAppointment && (_jsxs("div", { style: {
                                    marginTop: 18,
                                    background: "#ffffff",
                                    border: "1px solid #e2e8f0",
                                    borderRadius: 20,
                                    padding: 18,
                                    display: "grid",
                                    gap: 12,
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: "Quick Create Appointment" }), _jsx("input", { value: appointmentPatient, onChange: (e) => setAppointmentPatient(e.target.value), placeholder: "Patient name", style: inputStyle }), _jsx("input", { value: appointmentDepartment, onChange: (e) => setAppointmentDepartment(e.target.value), placeholder: "Department", style: inputStyle }), _jsx("input", { value: appointmentTime, onChange: (e) => setAppointmentTime(e.target.value), placeholder: "Time e.g. 2026-03-17 16:00", style: inputStyle }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("button", { onClick: handleCreateAppointment, disabled: creatingAppointment, style: {
                                                    padding: "10px 14px",
                                                    borderRadius: 12,
                                                    border: "none",
                                                    background: "#2563eb",
                                                    color: "white",
                                                    cursor: creatingAppointment ? "not-allowed" : "pointer",
                                                    opacity: creatingAppointment ? 0.7 : 1,
                                                    fontWeight: 800,
                                                }, children: creatingAppointment ? "Creating..." : "Save Appointment" }), _jsx("button", { onClick: () => setShowCreateAppointment(false), style: {
                                                    padding: "10px 14px",
                                                    borderRadius: 12,
                                                    border: "1px solid #cbd5e1",
                                                    background: "#fff",
                                                    color: "#0f172a",
                                                    cursor: "pointer",
                                                    fontWeight: 700,
                                                }, children: "Cancel" })] })] })), showQuickNote && (_jsxs("div", { style: {
                                    marginTop: 18,
                                    background: "#ffffff",
                                    border: "1px solid #e2e8f0",
                                    borderRadius: 20,
                                    padding: 18,
                                    display: "grid",
                                    gap: 12,
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: "Quick Clinical Note" }), _jsx("textarea", { value: quickNoteText, onChange: (e) => setQuickNoteText(e.target.value), placeholder: "Write a quick doctor note...", rows: 5, style: {
                                            ...inputStyle,
                                            resize: "vertical",
                                            minHeight: 120,
                                        } }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("button", { onClick: handleCreateQuickNote, style: {
                                                    padding: "10px 14px",
                                                    borderRadius: 12,
                                                    border: "none",
                                                    background: "#0f766e",
                                                    color: "white",
                                                    cursor: "pointer",
                                                    fontWeight: 800,
                                                }, children: "Save Note" }), _jsx("button", { onClick: () => setShowQuickNote(false), style: {
                                                    padding: "10px 14px",
                                                    borderRadius: 12,
                                                    border: "1px solid #cbd5e1",
                                                    background: "#fff",
                                                    color: "#0f172a",
                                                    cursor: "pointer",
                                                    fontWeight: 700,
                                                }, children: "Cancel" })] })] }))] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsxs("div", { className: "avoid-break", style: {
                                    background: "#f8fafc",
                                    color: "#0f172a",
                                    borderRadius: 26,
                                    padding: 22,
                                    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 14 }, children: "Performance Snapshot" }), _jsxs("div", { style: { display: "grid", gap: 12 }, children: [_jsx(MetricCard, { title: "Patients Today", value: String(doctor.patients) }), _jsx(MetricCard, { title: "Average Rating", value: `⭐ ${doctor.rating}` }), _jsx(MetricCard, { title: "Availability", value: doctor.status })] })] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "#f8fafc",
                                    color: "#0f172a",
                                    borderRadius: 26,
                                    padding: 22,
                                    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 14 }, children: "Assignment Dashboard" }), _jsxs("div", { style: {
                                            display: "grid",
                                            gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                                            gap: 12,
                                        }, children: [_jsx(SmallDashboardCard, { title: "Total", value: String(assignmentStats.total), tone: "#e0f2fe" }), _jsx(SmallDashboardCard, { title: "Assigned", value: String(assignmentStats.assigned), tone: "#dbeafe" }), _jsx(SmallDashboardCard, { title: "In Follow-up", value: String(assignmentStats.followUp), tone: "#fef3c7" }), _jsx(SmallDashboardCard, { title: "Completed", value: String(assignmentStats.completed), tone: "#dcfce7" })] })] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "#f8fafc",
                                    color: "#0f172a",
                                    borderRadius: 26,
                                    padding: 22,
                                    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                                }, children: [_jsxs("div", { style: {
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "space-between",
                                            gap: 12,
                                            marginBottom: 12,
                                        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: "Upcoming Appointments" }), _jsx("button", { onClick: () => navigate(`/appointments?doctorId=${encodeURIComponent(doctor.id)}&doctorName=${encodeURIComponent(doctor.name)}`), style: {
                                                    padding: "8px 12px",
                                                    borderRadius: 10,
                                                    border: "none",
                                                    background: "#2563eb",
                                                    color: "white",
                                                    cursor: "pointer",
                                                    fontWeight: 700,
                                                    fontSize: 12,
                                                }, children: "Open Appointments" })] }), appointments.length === 0 ? (_jsx("div", { style: { color: "#64748b" }, children: "No upcoming appointments found." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: appointments.map((item) => {
                                            const tone = appointmentTone(item.status);
                                            return (_jsx("div", { style: {
                                                    background: "white",
                                                    border: "1px solid #e2e8f0",
                                                    borderRadius: 16,
                                                    padding: 14,
                                                }, children: _jsxs("div", { style: {
                                                        display: "flex",
                                                        justifyContent: "space-between",
                                                        gap: 12,
                                                        flexWrap: "wrap",
                                                        alignItems: "start",
                                                    }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800 }, children: item.patient }), _jsx("div", { style: { color: "#64748b", marginTop: 4 }, children: item.department }), _jsx("div", { style: { color: "#64748b", marginTop: 4 }, children: item.time })] }), _jsx("div", { style: {
                                                                background: tone.bg,
                                                                color: tone.color,
                                                                padding: "6px 10px",
                                                                borderRadius: 999,
                                                                fontWeight: 800,
                                                                fontSize: 12,
                                                            }, children: item.status })] }) }, item.id));
                                        }) }))] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "#f8fafc",
                                    color: "#0f172a",
                                    borderRadius: 26,
                                    padding: 22,
                                    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 12 }, children: "Doctor Notes" }), doctorNotes.length === 0 ? (_jsx("div", { style: { color: "#64748b" }, children: "No quick notes yet." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: doctorNotes.map((note) => (_jsxs("div", { style: {
                                                background: "white",
                                                border: "1px solid #e2e8f0",
                                                borderRadius: 16,
                                                padding: 14,
                                            }, children: [_jsx("div", { style: { whiteSpace: "pre-wrap", lineHeight: 1.7 }, children: note.text }), _jsxs("div", { style: {
                                                        marginTop: 10,
                                                        display: "flex",
                                                        justifyContent: "space-between",
                                                        gap: 12,
                                                        alignItems: "center",
                                                        flexWrap: "wrap",
                                                    }, children: [_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: note.createdAt }), _jsx("button", { onClick: () => handleRemoveNote(note.id), style: smallActionButton("#b91c1c"), children: "Remove Note" })] })] }, note.id))) }))] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "#f8fafc",
                                    color: "#0f172a",
                                    borderRadius: 26,
                                    padding: 22,
                                    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 12 }, children: "Assigned Patients" }), assignments.length === 0 ? (_jsx("div", { style: { color: "#64748b" }, children: "No assigned patients yet." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: assignments.map((item) => {
                                            const tone = assignmentTone(item.status);
                                            return (_jsxs("div", { style: {
                                                    background: "white",
                                                    border: "1px solid #e2e8f0",
                                                    borderRadius: 16,
                                                    padding: 14,
                                                }, children: [_jsxs("div", { style: {
                                                            display: "flex",
                                                            justifyContent: "space-between",
                                                            gap: 12,
                                                            alignItems: "start",
                                                            flexWrap: "wrap",
                                                        }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800 }, children: item.patientName }), _jsxs("div", { style: { color: "#64748b", marginTop: 4 }, children: [item.patientId, " \u2022 ", item.department ?? "No department"] }), _jsx("div", { style: { color: "#64748b", marginTop: 4 }, children: item.condition ?? "No condition" })] }), _jsx("div", { style: {
                                                                    background: tone.bg,
                                                                    color: tone.color,
                                                                    padding: "6px 10px",
                                                                    borderRadius: 999,
                                                                    fontWeight: 800,
                                                                    fontSize: 12,
                                                                }, children: item.status ?? "Assigned" })] }), _jsxs("div", { style: {
                                                            marginTop: 12,
                                                            display: "flex",
                                                            gap: 8,
                                                            flexWrap: "wrap",
                                                        }, children: [_jsx("button", { onClick: () => handleStatusChange(item.id, "Assigned"), disabled: busyId === item.id, style: smallActionButton("#2563eb"), children: "Assigned" }), _jsx("button", { onClick: () => handleStatusChange(item.id, "In Follow-up"), disabled: busyId === item.id, style: smallActionButton("#d97706"), children: "In Follow-up" }), _jsx("button", { onClick: () => handleStatusChange(item.id, "Completed"), disabled: busyId === item.id, style: smallActionButton("#15803d"), children: "Completed" }), _jsx("button", { onClick: () => handleRemove(item.id), disabled: busyId === item.id, style: smallActionButton("#b91c1c"), children: "Remove" })] })] }, item.id));
                                        }) }))] }), _jsxs("div", { className: "avoid-break", style: {
                                    background: "#ecfeff",
                                    color: "#0f172a",
                                    border: "1px solid #a5f3fc",
                                    borderRadius: 26,
                                    padding: 22,
                                }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 12 }, children: "Recommended Actions" }), _jsxs("ul", { style: { margin: 0, paddingLeft: 18, lineHeight: 1.9, color: "#155e75" }, children: [_jsx("li", { children: "Review live schedule and on-call responsibilities." }), _jsx("li", { children: "Open specialty dashboard for related department workflow." }), _jsx("li", { children: "Monitor patient load and staffing balance." })] })] })] })] }))] }));
}
function InfoRow({ label, value }) {
    return (_jsxs("div", { style: {
            display: "flex",
            justifyContent: "space-between",
            gap: 16,
            borderBottom: "1px solid #f1f5f9",
            paddingBottom: 10,
        }, children: [_jsx("div", { style: { color: "#64748b" }, children: label }), _jsx("div", { style: { fontWeight: 700, textAlign: "right" }, children: value })] }));
}
function MetricCard({ title, value }) {
    return (_jsxs("div", { style: {
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 18,
            padding: 16,
        }, children: [_jsx("div", { style: { color: "#64748b", marginBottom: 10 }, children: title }), _jsx("div", { style: { fontSize: 26, fontWeight: 800 }, children: value })] }));
}
function SmallDashboardCard({ title, value, tone, }) {
    return (_jsxs("div", { style: {
            background: tone,
            borderRadius: 18,
            padding: 16,
        }, children: [_jsx("div", { style: { color: "#475569", marginBottom: 8 }, children: title }), _jsx("div", { style: { fontSize: 26, fontWeight: 800 }, children: value })] }));
}
function smallActionButton(background) {
    return {
        padding: "8px 10px",
        borderRadius: 10,
        border: "none",
        background,
        color: "white",
        cursor: "pointer",
        fontWeight: 700,
        fontSize: 12,
    };
}
const inputStyle = {
    width: "100%",
    padding: "12px 14px",
    borderRadius: 12,
    border: "1px solid #cbd5e1",
    background: "white",
    color: "#0f172a",
};
