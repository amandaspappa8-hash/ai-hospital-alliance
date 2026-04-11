import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiGet, apiPost } from "@/lib/api";
export default function AppointmentsPage() {
    const [searchParams] = useSearchParams();
    const doctorId = searchParams.get("doctorId") ?? "";
    const doctorName = searchParams.get("doctorName") ?? "";
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [saving, setSaving] = useState(false);
    const [form, setForm] = useState({
        patient: "",
        department: "",
        doctor: doctorName || "",
        time: "",
        status: "Scheduled",
    });
    useEffect(() => {
        setLoading(true);
        setError("");
        apiGet("/appointments")
            .then((data) => {
            setAppointments(Array.isArray(data) ? data : []);
        })
            .catch((err) => {
            setError(err instanceof Error ? err.message : "Failed to load appointments");
        })
            .finally(() => {
            setLoading(false);
        });
    }, []);
    useEffect(() => {
        if (doctorName) {
            setForm((prev) => ({
                ...prev,
                doctor: doctorName,
            }));
        }
    }, [doctorName]);
    const filteredAppointments = useMemo(() => {
        if (!doctorName && !doctorId)
            return appointments;
        return appointments.filter((appointment) => {
            if (doctorName) {
                return appointment.doctor.toLowerCase() === doctorName.toLowerCase();
            }
            return true;
        });
    }, [appointments, doctorId, doctorName]);
    function handleChange(e) {
        const { name, value } = e.target;
        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    }
    async function handleCreateAppointment(e) {
        e.preventDefault();
        if (!form.patient.trim() ||
            !form.department.trim() ||
            !form.doctor.trim() ||
            !form.time.trim() ||
            !form.status.trim()) {
            setError("Please fill in all appointment fields.");
            return;
        }
        try {
            setSaving(true);
            setError("");
            const payload = {
                patient: form.patient.trim(),
                department: form.department.trim(),
                doctor: form.doctor.trim(),
                time: form.time,
                status: form.status.trim(),
            };
            const created = await apiPost("/appointments", payload);
            setAppointments((prev) => [created, ...prev]);
            setForm({
                patient: "",
                department: "",
                doctor: doctorName || "",
                time: "",
                status: "Scheduled",
            });
            setShowCreateForm(false);
        }
        catch (err) {
            setError(err instanceof Error ? err.message : "Failed to create appointment");
        }
        finally {
            setSaving(false);
        }
    }
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold", children: "Appointments" }), _jsx("p", { className: "text-sm text-gray-500", children: doctorName
                                    ? `Managing appointments for Dr. ${doctorName}`
                                    : "Manage all appointments from one page" })] }), _jsx("button", { onClick: () => setShowCreateForm((prev) => !prev), className: "rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700", children: showCreateForm ? "Close Form" : "Create Appointment" })] }), error && (_jsx("div", { className: "rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-red-700", children: error })), showCreateForm && (_jsxs("form", { onSubmit: handleCreateAppointment, className: "grid gap-4 rounded-xl border bg-white p-5 shadow-sm md:grid-cols-2", children: [_jsxs("div", { children: [_jsx("label", { className: "mb-1 block text-sm font-medium", children: "Patient Name" }), _jsx("input", { name: "patient", value: form.patient, onChange: handleChange, placeholder: "Enter patient name", className: "w-full rounded-lg border px-3 py-2" })] }), _jsxs("div", { children: [_jsx("label", { className: "mb-1 block text-sm font-medium", children: "Department" }), _jsx("input", { name: "department", value: form.department, onChange: handleChange, placeholder: "Enter department", className: "w-full rounded-lg border px-3 py-2" })] }), _jsxs("div", { children: [_jsx("label", { className: "mb-1 block text-sm font-medium", children: "Doctor" }), _jsx("input", { name: "doctor", value: form.doctor, onChange: handleChange, placeholder: "Enter doctor name", className: "w-full rounded-lg border px-3 py-2" })] }), _jsxs("div", { children: [_jsx("label", { className: "mb-1 block text-sm font-medium", children: "Time" }), _jsx("input", { type: "datetime-local", name: "time", value: form.time, onChange: handleChange, className: "w-full rounded-lg border px-3 py-2" })] }), _jsxs("div", { children: [_jsx("label", { className: "mb-1 block text-sm font-medium", children: "Status" }), _jsxs("select", { name: "status", value: form.status, onChange: handleChange, className: "w-full rounded-lg border px-3 py-2", children: [_jsx("option", { value: "Scheduled", children: "Scheduled" }), _jsx("option", { value: "Confirmed", children: "Confirmed" }), _jsx("option", { value: "Pending", children: "Pending" }), _jsx("option", { value: "Completed", children: "Completed" }), _jsx("option", { value: "Cancelled", children: "Cancelled" })] })] }), _jsxs("div", { className: "md:col-span-2 flex gap-3", children: [_jsx("button", { type: "submit", disabled: saving, className: "rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-60", children: saving ? "Saving..." : "Save Appointment" }), _jsx("button", { type: "button", onClick: () => setShowCreateForm(false), className: "rounded-lg border px-4 py-2 hover:bg-gray-50", children: "Cancel" })] })] })), _jsx("div", { className: "rounded-xl border bg-white shadow-sm", children: loading ? (_jsx("div", { className: "p-6 text-sm text-gray-500", children: "Loading appointments..." })) : filteredAppointments.length === 0 ? (_jsx("div", { className: "p-6 text-sm text-gray-500", children: "No appointments found." })) : (_jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "min-w-full border-collapse text-sm", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b bg-gray-50 text-left", children: [_jsx("th", { className: "px-4 py-3", children: "Patient" }), _jsx("th", { className: "px-4 py-3", children: "Department" }), _jsx("th", { className: "px-4 py-3", children: "Doctor" }), _jsx("th", { className: "px-4 py-3", children: "Time" }), _jsx("th", { className: "px-4 py-3", children: "Status" })] }) }), _jsx("tbody", { children: filteredAppointments.map((appointment) => (_jsxs("tr", { className: "border-b last:border-0", children: [_jsx("td", { className: "px-4 py-3", children: appointment.patient }), _jsx("td", { className: "px-4 py-3", children: appointment.department }), _jsx("td", { className: "px-4 py-3", children: appointment.doctor }), _jsx("td", { className: "px-4 py-3", children: appointment.time }), _jsx("td", { className: "px-4 py-3", children: appointment.status })] }, appointment.id))) })] }) })) })] }));
}
