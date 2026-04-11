import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
export default function Dashboard() {
    const [patientsCount, setPatientsCount] = useState(0);
    const [appointmentsCount, setAppointmentsCount] = useState(0);
    const [reportsCount, setReportsCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        async function loadDashboard() {
            try {
                const [patients, appointments, reports] = await Promise.all([
                    apiGet("/patients"),
                    apiGet("/appointments"),
                    apiGet("/reports"),
                ]);
                setPatientsCount(Array.isArray(patients) ? patients.length : 0);
                setAppointmentsCount(Array.isArray(appointments) ? appointments.length : 0);
                setReportsCount(Array.isArray(reports) ? reports.length : 0);
            }
            catch (err) {
                console.error(err);
                setError("Failed to load dashboard data");
            }
            finally {
                setLoading(false);
            }
        }
        loadDashboard();
    }, []);
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Smart Hospital Dashboard" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Welcome, System Admin \u2014 Admin" }), error && _jsx("div", { style: { color: "#fca5a5", marginBottom: "16px" }, children: error }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
                    gap: "16px",
                }, children: [_jsx(StatCard, { title: "Patients", value: loading ? "..." : String(patientsCount) }), _jsx(StatCard, { title: "Appointments", value: loading ? "..." : String(appointmentsCount) }), _jsx(StatCard, { title: "Pending Reports", value: loading ? "..." : String(reportsCount) })] })] }));
}
function StatCard({ title, value }) {
    return (_jsxs("div", { style: {
            background: "#111827",
            border: "1px solid #374151",
            borderRadius: "14px",
            padding: "22px",
            minHeight: "140px",
        }, children: [_jsx("div", { style: { opacity: 0.8, marginBottom: "18px" }, children: title }), _jsx("div", { style: { fontSize: "42px", fontWeight: 700 }, children: value })] }));
}
