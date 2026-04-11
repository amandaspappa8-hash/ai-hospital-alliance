import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, } from "recharts";
import { apiGet } from "@/lib/api";
import { getDoctorsSummary } from "@/lib/doctors";
import { getSpecialtiesSummary } from "@/lib/specialties";
import { getDoctorAssignments } from "@/lib/doctorAssignments";
export default function AdminOverviewPage() {
    const [doctors, setDoctors] = useState([]);
    const [specialties, setSpecialties] = useState([]);
    const [patientsCount, setPatientsCount] = useState(0);
    const [appointments, setAppointments] = useState([]);
    const [reports, setReports] = useState([]);
    const [assignedPatientsCount, setAssignedPatientsCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        async function loadOverview() {
            try {
                setLoading(true);
                setError("");
                const [doctorsData, specialtiesData, patientsData, appointmentsData, reportsData] = await Promise.all([
                    getDoctorsSummary(),
                    getSpecialtiesSummary(),
                    apiGet("/patients"),
                    apiGet("/appointments"),
                    apiGet("/reports"),
                ]);
                setDoctors(doctorsData);
                setSpecialties(specialtiesData);
                setPatientsCount(Array.isArray(patientsData) ? patientsData.length : 0);
                setAppointments(Array.isArray(appointmentsData) ? appointmentsData : []);
                setReports(Array.isArray(reportsData) ? reportsData : []);
                const assignmentLists = await Promise.all(doctorsData.map((doctor) => getDoctorAssignments(doctor.id)));
                const totalAssigned = assignmentLists.reduce((sum, items) => sum + items.length, 0);
                setAssignedPatientsCount(totalAssigned);
            }
            catch (err) {
                console.error(err);
                setError("Failed to load admin overview");
            }
            finally {
                setLoading(false);
            }
        }
        loadOverview();
    }, []);
    const availableDoctors = useMemo(() => doctors.filter((doctor) => doctor.status === "Available").length, [doctors]);
    const onCallDoctors = useMemo(() => doctors.filter((doctor) => doctor.status === "On Call").length, [doctors]);
    const busyDoctors = useMemo(() => doctors.filter((doctor) => doctor.status === "In Surgery" || doctor.status === "Offline").length, [doctors]);
    const specialtyBreakdown = useMemo(() => {
        const map = new Map();
        doctors.forEach((doctor) => {
            map.set(doctor.specialty, (map.get(doctor.specialty) ?? 0) + 1);
        });
        return Array.from(map.entries())
            .map(([name, count]) => ({ name, count }))
            .sort((a, b) => b.count - a.count);
    }, [doctors]);
    const doctorStatusData = useMemo(() => {
        const available = doctors.filter((d) => d.status === "Available").length;
        const onCall = doctors.filter((d) => d.status === "On Call").length;
        const inSurgery = doctors.filter((d) => d.status === "In Surgery").length;
        const offline = doctors.filter((d) => d.status === "Offline").length;
        return [
            { name: "Available", value: available, color: "#22c55e" },
            { name: "On Call", value: onCall, color: "#f59e0b" },
            { name: "In Surgery", value: inSurgery, color: "#ef4444" },
            { name: "Offline", value: offline, color: "#94a3b8" },
        ];
    }, [doctors]);
    const appointmentsStatusData = useMemo(() => {
        const map = new Map();
        appointments.forEach((item) => {
            const key = item.status || "Unknown";
            map.set(key, (map.get(key) ?? 0) + 1);
        });
        return Array.from(map.entries()).map(([name, value], index) => ({
            name,
            value,
            color: ["#3b82f6", "#f59e0b", "#22c55e", "#94a3b8", "#a855f7"][index % 5],
        }));
    }, [appointments]);
    const reportsStatusData = useMemo(() => {
        const map = new Map();
        reports.forEach((item) => {
            const key = item.status || "Unknown";
            map.set(key, (map.get(key) ?? 0) + 1);
        });
        return Array.from(map.entries()).map(([name, value], index) => ({
            name,
            value,
            color: ["#8b5cf6", "#06b6d4", "#22c55e", "#f97316", "#94a3b8"][index % 5],
        }));
    }, [reports]);
    const topSpecialties = useMemo(() => {
        return [...specialties]
            .sort((a, b) => b.activeCases - a.activeCases)
            .slice(0, 4);
    }, [specialties]);
    return (_jsxs("div", { style: { padding: 24, color: "#e5eef8" }, children: [_jsxs("div", { style: { marginBottom: 22 }, children: [_jsx("div", { style: { fontSize: 32, fontWeight: 800, marginBottom: 6 }, children: "Admin Overview" }), _jsx("div", { style: { opacity: 0.8 }, children: "Executive hospital summary across doctors, specialties, patients, appointments, and reports" })] }), error && _jsx("div", { style: { color: "#fecaca", marginBottom: 16 }, children: error }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                    gap: 16,
                    marginBottom: 20,
                }, children: [_jsx(StatCard, { title: "Doctors", value: loading ? "..." : String(doctors.length), tone: "#17212f", text: "#ffffff" }), _jsx(StatCard, { title: "Specialties", value: loading ? "..." : String(specialties.length), tone: "#e0f2fe", text: "#0f172a" }), _jsx(StatCard, { title: "Patients", value: loading ? "..." : String(patientsCount), tone: "#dcfce7", text: "#0f172a" }), _jsx(StatCard, { title: "Appointments", value: loading ? "..." : String(appointments.length), tone: "#fef3c7", text: "#0f172a" })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                    gap: 16,
                    marginBottom: 24,
                }, children: [_jsx(StatCard, { title: "Reports", value: loading ? "..." : String(reports.length), tone: "#ede9fe", text: "#0f172a" }), _jsx(StatCard, { title: "Assigned Patients", value: loading ? "..." : String(assignedPatientsCount), tone: "#fee2e2", text: "#0f172a" }), _jsx(StatCard, { title: "Available Doctors", value: loading ? "..." : String(availableDoctors), tone: "#d1fae5", text: "#0f172a" }), _jsx(StatCard, { title: "On Call / Busy", value: loading ? "..." : `${onCallDoctors} / ${busyDoctors}`, tone: "#f8fafc", text: "#0f172a" })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "1.25fr 1fr",
                    gap: 20,
                    marginBottom: 20,
                }, children: [_jsx(Panel, { title: "Doctors by Specialty Chart", children: _jsx("div", { style: { width: "100%", height: 320 }, children: !loading && specialtyBreakdown.length > 0 ? (_jsx(ResponsiveContainer, { width: "100%", height: "100%", children: _jsxs(BarChart, { data: specialtyBreakdown, children: [_jsx(XAxis, { dataKey: "name", tick: { fill: "#475569", fontSize: 12 } }), _jsx(YAxis, { tick: { fill: "#475569", fontSize: 12 } }), _jsx(Tooltip, {}), _jsx(Bar, { dataKey: "count", radius: [8, 8, 0, 0], fill: "#60a5fa" })] }) })) : (_jsx(CenteredState, { loading: loading, emptyText: "No chart data available." })) }) }), _jsxs(Panel, { title: "Doctor Status Distribution", children: [_jsx("div", { style: { width: "100%", height: 320 }, children: !loading && doctorStatusData.some((item) => item.value > 0) ? (_jsx(ResponsiveContainer, { width: "100%", height: "100%", children: _jsxs(PieChart, { children: [_jsx(Pie, { data: doctorStatusData, dataKey: "value", nameKey: "name", cx: "50%", cy: "50%", outerRadius: 95, innerRadius: 55, paddingAngle: 3, children: doctorStatusData.map((entry) => (_jsx(Cell, { fill: entry.color }, entry.name))) }), _jsx(Tooltip, {})] }) })) : (_jsx(CenteredState, { loading: loading, emptyText: "No status data available." })) }), _jsx("div", { style: { display: "grid", gap: 10, marginTop: 10 }, children: doctorStatusData.map((item) => (_jsx(LegendRow, { color: item.color, name: item.name, value: item.value }, item.name))) })] })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 20,
                    marginBottom: 20,
                }, children: [_jsxs(Panel, { title: "Appointments Status Breakdown", children: [_jsx("div", { style: { width: "100%", height: 300 }, children: !loading && appointmentsStatusData.length > 0 ? (_jsx(ResponsiveContainer, { width: "100%", height: "100%", children: _jsxs(PieChart, { children: [_jsx(Pie, { data: appointmentsStatusData, dataKey: "value", nameKey: "name", cx: "50%", cy: "50%", outerRadius: 95, innerRadius: 52, paddingAngle: 3, children: appointmentsStatusData.map((entry) => (_jsx(Cell, { fill: entry.color }, entry.name))) }), _jsx(Tooltip, {})] }) })) : (_jsx(CenteredState, { loading: loading, emptyText: "No appointment status data." })) }), _jsx("div", { style: { display: "grid", gap: 10, marginTop: 10 }, children: appointmentsStatusData.map((item) => (_jsx(LegendRow, { color: item.color, name: item.name, value: item.value }, item.name))) })] }), _jsxs(Panel, { title: "Reports Status Breakdown", children: [_jsx("div", { style: { width: "100%", height: 300 }, children: !loading && reportsStatusData.length > 0 ? (_jsx(ResponsiveContainer, { width: "100%", height: "100%", children: _jsxs(PieChart, { children: [_jsx(Pie, { data: reportsStatusData, dataKey: "value", nameKey: "name", cx: "50%", cy: "50%", outerRadius: 95, innerRadius: 52, paddingAngle: 3, children: reportsStatusData.map((entry) => (_jsx(Cell, { fill: entry.color }, entry.name))) }), _jsx(Tooltip, {})] }) })) : (_jsx(CenteredState, { loading: loading, emptyText: "No report status data." })) }), _jsx("div", { style: { display: "grid", gap: 10, marginTop: 10 }, children: reportsStatusData.map((item) => (_jsx(LegendRow, { color: item.color, name: item.name, value: item.value }, item.name))) })] })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "1.2fr 1fr",
                    gap: 20,
                }, children: [_jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsx(Panel, { title: "Doctors by Specialty", children: loading ? (_jsx("div", { children: "Loading..." })) : specialtyBreakdown.length === 0 ? (_jsx("div", { children: "No specialty data found." })) : (_jsx("div", { style: { display: "grid", gap: 10 }, children: specialtyBreakdown.map((item) => (_jsxs("div", { style: {
                                            background: "white",
                                            border: "1px solid #e2e8f0",
                                            borderRadius: 16,
                                            padding: 14,
                                            display: "flex",
                                            justifyContent: "space-between",
                                            alignItems: "center",
                                            gap: 12,
                                        }, children: [_jsx("div", { style: { fontWeight: 800 }, children: item.name }), _jsxs("div", { style: {
                                                    background: "#eff6ff",
                                                    color: "#1d4ed8",
                                                    borderRadius: 999,
                                                    padding: "6px 10px",
                                                    fontWeight: 800,
                                                    fontSize: 12,
                                                }, children: [item.count, " doctors"] })] }, item.name))) })) }), _jsx(Panel, { title: "Top Active Specialties", children: loading ? (_jsx("div", { children: "Loading..." })) : topSpecialties.length === 0 ? (_jsx("div", { children: "No specialty activity found." })) : (_jsx("div", { style: { display: "grid", gap: 12 }, children: topSpecialties.map((item) => (_jsxs("div", { style: {
                                            background: "white",
                                            border: "1px solid #e2e8f0",
                                            borderRadius: 18,
                                            padding: 16,
                                        }, children: [_jsxs("div", { style: {
                                                    display: "flex",
                                                    justifyContent: "space-between",
                                                    gap: 12,
                                                    alignItems: "center",
                                                    marginBottom: 8,
                                                }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 17 }, children: [item.icon, " ", item.title] }), _jsxs("div", { style: {
                                                            background: "#ecfeff",
                                                            color: "#0f766e",
                                                            borderRadius: 999,
                                                            padding: "6px 10px",
                                                            fontWeight: 800,
                                                            fontSize: 12,
                                                        }, children: [item.activeCases, " active cases"] })] }), _jsx("div", { style: { color: "#64748b", marginBottom: 10 }, children: item.subtitle }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx(Badge, { text: `${item.doctors} doctors`, tone: "#eff6ff", color: "#1d4ed8" }), _jsx(Badge, { text: item.route, tone: "#f8fafc", color: "#334155" })] })] }, item.title))) })) })] }), _jsxs("div", { style: { display: "grid", gap: 20 }, children: [_jsx(Panel, { title: "System Status", children: _jsxs("div", { style: { display: "grid", gap: 12 }, children: [_jsx(StatusRow, { label: "Doctors Service", value: "Operational", tone: "#dcfce7", color: "#166534" }), _jsx(StatusRow, { label: "Specialties Data", value: "Synced", tone: "#dbeafe", color: "#1d4ed8" }), _jsx(StatusRow, { label: "Appointments", value: "Live", tone: "#fef3c7", color: "#92400e" }), _jsx(StatusRow, { label: "Reports", value: "Available", tone: "#ede9fe", color: "#6d28d9" }), _jsx(StatusRow, { label: "Assignments", value: "Tracked", tone: "#ecfeff", color: "#0f766e" })] }) }), _jsx(Panel, { title: "Hospital Snapshot", children: _jsxs("div", { style: { display: "grid", gap: 12 }, children: [_jsx(SnapshotCard, { title: "Average Appointments per Doctor", value: loading || doctors.length === 0 ? "..." : (appointments.length / doctors.length).toFixed(1) }), _jsx(SnapshotCard, { title: "Average Assigned Patients per Doctor", value: loading || doctors.length === 0 ? "..." : (assignedPatientsCount / doctors.length).toFixed(1) }), _jsx(SnapshotCard, { title: "Reports per Patient Ratio", value: loading || patientsCount === 0 ? "..." : (reports.length / patientsCount).toFixed(2) })] }) })] })] })] }));
}
function CenteredState({ loading, emptyText, }) {
    return (_jsx("div", { style: {
            width: "100%",
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#64748b",
            fontWeight: 600,
        }, children: loading ? "Loading..." : emptyText }));
}
function LegendRow({ color, name, value, }) {
    return (_jsxs("div", { style: {
            display: "flex",
            justifyContent: "space-between",
            gap: 12,
            alignItems: "center",
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 14,
            padding: "10px 12px",
        }, children: [_jsxs("div", { style: { display: "flex", alignItems: "center", gap: 10 }, children: [_jsx("span", { style: {
                            width: 12,
                            height: 12,
                            borderRadius: 999,
                            background: color,
                            display: "inline-block",
                        } }), _jsx("span", { style: { fontWeight: 700 }, children: name })] }), _jsx("span", { style: { fontWeight: 800 }, children: value })] }));
}
function Panel({ title, children, }) {
    return (_jsxs("div", { style: {
            background: "#f8fafc",
            color: "#0f172a",
            borderRadius: 26,
            padding: 22,
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 14 }, children: title }), children] }));
}
function StatCard({ title, value, tone, text, }) {
    return (_jsxs("div", { style: {
            background: tone,
            color: text,
            borderRadius: 22,
            padding: 20,
            minHeight: 118,
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
        }, children: [_jsx("div", { style: { opacity: 0.8, marginBottom: 18 }, children: title }), _jsx("div", { style: { fontSize: 34, fontWeight: 800 }, children: value })] }));
}
function Badge({ text, tone, color, }) {
    return (_jsx("div", { style: {
            background: tone,
            color,
            borderRadius: 999,
            padding: "8px 12px",
            fontWeight: 700,
            fontSize: 13,
        }, children: text }));
}
function StatusRow({ label, value, tone, color, }) {
    return (_jsxs("div", { style: {
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 16,
            padding: 14,
            display: "flex",
            justifyContent: "space-between",
            gap: 12,
            alignItems: "center",
        }, children: [_jsx("div", { style: { fontWeight: 700 }, children: label }), _jsx("div", { style: {
                    background: tone,
                    color,
                    borderRadius: 999,
                    padding: "6px 10px",
                    fontWeight: 800,
                    fontSize: 12,
                }, children: value })] }));
}
function SnapshotCard({ title, value, }) {
    return (_jsxs("div", { style: {
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 18,
            padding: 16,
        }, children: [_jsx("div", { style: { color: "#64748b", marginBottom: 10 }, children: title }), _jsx("div", { style: { fontSize: 28, fontWeight: 800 }, children: value })] }));
}
