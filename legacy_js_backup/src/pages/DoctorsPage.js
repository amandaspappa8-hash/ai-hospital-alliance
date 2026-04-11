import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDoctorsSummary } from "@/lib/doctors";
function statusColor(status) {
    if (status === "Available")
        return { bg: "#dcfce7", color: "#166534" };
    if (status === "On Call")
        return { bg: "#fef3c7", color: "#92400e" };
    if (status === "In Surgery")
        return { bg: "#fee2e2", color: "#991b1b" };
    return { bg: "#e5e7eb", color: "#374151" };
}
export default function DoctorsPage() {
    const navigate = useNavigate();
    const [doctors, setDoctors] = useState([]);
    const [query, setQuery] = useState("");
    const [specialty, setSpecialty] = useState("All");
    const [selectedDoctorId, setSelectedDoctorId] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        async function loadDoctors() {
            try {
                setLoading(true);
                setError("");
                const data = await getDoctorsSummary();
                setDoctors(data);
                if (data.length > 0) {
                    setSelectedDoctorId(data[0].id);
                }
            }
            catch (err) {
                console.error(err);
                setError("Failed to load doctors");
                setDoctors([]);
            }
            finally {
                setLoading(false);
            }
        }
        loadDoctors();
    }, []);
    const specialties = useMemo(() => {
        const values = Array.from(new Set(doctors.map((d) => d.specialty)));
        return ["All", ...values];
    }, [doctors]);
    const filteredDoctors = useMemo(() => {
        const q = query.trim().toLowerCase();
        return doctors.filter((doctor) => {
            const matchesQuery = !q ||
                doctor.name.toLowerCase().includes(q) ||
                doctor.specialty.toLowerCase().includes(q) ||
                doctor.department.toLowerCase().includes(q);
            const matchesSpecialty = specialty === "All" || doctor.specialty === specialty;
            return matchesQuery && matchesSpecialty;
        });
    }, [doctors, query, specialty]);
    const selectedDoctor = filteredDoctors.find((doctor) => doctor.id === selectedDoctorId) ||
        doctors.find((doctor) => doctor.id === selectedDoctorId) ||
        filteredDoctors[0] ||
        null;
    const availableCount = doctors.filter((d) => d.status === "Available").length;
    const totalPatients = doctors.reduce((sum, d) => sum + d.patients, 0);
    const avgRating = doctors.length
        ? (doctors.reduce((sum, d) => sum + d.rating, 0) / doctors.length).toFixed(1)
        : "0.0";
    return (_jsxs("div", { style: { padding: 24, color: "#e5eef8" }, children: [_jsxs("div", { style: { marginBottom: 22 }, children: [_jsx("div", { style: { fontSize: 32, fontWeight: 800, marginBottom: 6 }, children: "Doctors & Specialties" }), _jsx("div", { style: { opacity: 0.8 }, children: "Smart clinical workforce dashboard for all departments" })] }), error && _jsx("div", { style: { color: "#fecaca", marginBottom: 16 }, children: error }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                    gap: 16,
                    marginBottom: 20,
                }, children: [_jsx(TopStatCard, { title: "Total Doctors", value: loading ? "..." : String(doctors.length), tone: "dark" }), _jsx(TopStatCard, { title: "Available Now", value: loading ? "..." : String(availableCount), tone: "green" }), _jsx(TopStatCard, { title: "Patients Today", value: loading ? "..." : String(totalPatients), tone: "blue" }), _jsx(TopStatCard, { title: "Average Rating", value: loading ? "..." : String(avgRating), tone: "light" })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "2fr 1fr",
                    gap: 18,
                    marginBottom: 18,
                }, children: [_jsxs("div", { style: {
                            background: "#f8fafc",
                            borderRadius: 26,
                            padding: 24,
                            color: "#0f172a",
                            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.10)",
                        }, children: [_jsxs("div", { style: {
                                    display: "flex",
                                    justifyContent: "space-between",
                                    gap: 14,
                                    flexWrap: "wrap",
                                    marginBottom: 20,
                                }, children: [_jsxs("div", { children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800 }, children: "Doctor Directory" }), _jsx("div", { style: { color: "#64748b", marginTop: 4 }, children: "Search doctors by name, specialty, or department" })] }), _jsxs("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" }, children: [_jsx("input", { value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Search doctor...", style: {
                                                    padding: "12px 14px",
                                                    borderRadius: 14,
                                                    border: "1px solid #dbeafe",
                                                    minWidth: 220,
                                                    background: "white",
                                                } }), _jsx("select", { value: specialty, onChange: (e) => setSpecialty(e.target.value), style: {
                                                    padding: "12px 14px",
                                                    borderRadius: 14,
                                                    border: "1px solid #dbeafe",
                                                    minWidth: 180,
                                                    background: "white",
                                                }, children: specialties.map((item) => (_jsx("option", { children: item }, item))) })] })] }), _jsx("div", { style: { display: "grid", gap: 12 }, children: loading ? (_jsx("div", { children: "Loading doctors..." })) : filteredDoctors.length === 0 ? (_jsx("div", { children: "No doctors found." })) : (filteredDoctors.map((doctor) => {
                                    const tone = statusColor(doctor.status);
                                    const active = selectedDoctor?.id === doctor.id;
                                    return (_jsx("button", { onClick: () => setSelectedDoctorId(doctor.id), style: {
                                            textAlign: "left",
                                            width: "100%",
                                            border: active ? "2px solid #93c5fd" : "1px solid #e2e8f0",
                                            background: active ? "#eff6ff" : "white",
                                            borderRadius: 18,
                                            padding: 16,
                                            cursor: "pointer",
                                        }, children: _jsxs("div", { style: {
                                                display: "grid",
                                                gridTemplateColumns: "64px 1fr auto",
                                                alignItems: "center",
                                                gap: 14,
                                            }, children: [_jsx("div", { style: {
                                                        width: 64,
                                                        height: 64,
                                                        borderRadius: "50%",
                                                        background: "#dbeafe",
                                                        color: "#1d4ed8",
                                                        display: "flex",
                                                        alignItems: "center",
                                                        justifyContent: "center",
                                                        fontWeight: 800,
                                                        fontSize: 22,
                                                    }, children: doctor.name
                                                        .split(" ")
                                                        .slice(0, 2)
                                                        .map((p) => p[0])
                                                        .join("") }), _jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800, fontSize: 17 }, children: doctor.name }), _jsxs("div", { style: { color: "#475569", marginTop: 4 }, children: [doctor.specialty, " \u2022 ", doctor.department] }), _jsxs("div", { style: { color: "#64748b", marginTop: 6, fontSize: 13 }, children: ["Experience: ", doctor.experience, " \u2022 Patients today: ", doctor.patients] })] }), _jsxs("div", { style: { textAlign: "right" }, children: [_jsx("div", { style: {
                                                                display: "inline-block",
                                                                background: tone.bg,
                                                                color: tone.color,
                                                                padding: "6px 10px",
                                                                borderRadius: 999,
                                                                fontWeight: 800,
                                                                fontSize: 12,
                                                                marginBottom: 10,
                                                            }, children: doctor.status }), _jsxs("div", { style: { color: "#0f172a", fontWeight: 700 }, children: ["\u2B50 ", doctor.rating] })] })] }) }, doctor.id));
                                })) })] }), _jsxs("div", { style: {
                            background: "#f8fafc",
                            borderRadius: 26,
                            padding: 20,
                            color: "#0f172a",
                            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.10)",
                        }, children: [_jsx("div", { style: { fontSize: 18, fontWeight: 800, marginBottom: 14 }, children: "Featured Doctor" }), !selectedDoctor ? (_jsx("div", { children: "No doctor selected." })) : (_jsxs(_Fragment, { children: [_jsxs("div", { style: {
                                            background: "#eaffd0",
                                            borderRadius: 22,
                                            padding: 18,
                                            marginBottom: 16,
                                        }, children: [_jsx("div", { style: {
                                                    width: 140,
                                                    height: 140,
                                                    borderRadius: 24,
                                                    background: "white",
                                                    margin: "0 auto 16px auto",
                                                    display: "flex",
                                                    alignItems: "center",
                                                    justifyContent: "center",
                                                    fontSize: 42,
                                                    fontWeight: 800,
                                                    color: "#0f172a",
                                                    border: "1px solid #d9f99d",
                                                }, children: selectedDoctor.name
                                                    .split(" ")
                                                    .slice(0, 2)
                                                    .map((p) => p[0])
                                                    .join("") }), _jsx("div", { style: { textAlign: "center", fontWeight: 800, fontSize: 24 }, children: selectedDoctor.name }), _jsx("div", { style: { textAlign: "center", color: "#3f6212", marginTop: 6 }, children: selectedDoctor.specialty })] }), _jsxs("div", { style: {
                                            background: "white",
                                            border: "1px solid #e2e8f0",
                                            borderRadius: 18,
                                            padding: 16,
                                            display: "grid",
                                            gap: 10,
                                            marginBottom: 14,
                                        }, children: [_jsx(InfoRow, { label: "Department", value: selectedDoctor.department }), _jsx(InfoRow, { label: "Experience", value: selectedDoctor.experience }), _jsx(InfoRow, { label: "Schedule", value: selectedDoctor.schedule }), _jsx(InfoRow, { label: "Phone", value: selectedDoctor.phone }), _jsx(InfoRow, { label: "Patients Today", value: String(selectedDoctor.patients) }), _jsx(InfoRow, { label: "Rating", value: `⭐ ${selectedDoctor.rating}` })] }), _jsx("button", { onClick: () => navigate(`/doctors/${selectedDoctor.id}`), style: {
                                            width: "100%",
                                            padding: "14px 16px",
                                            borderRadius: 999,
                                            border: "none",
                                            background: "#0f172a",
                                            color: "white",
                                            fontWeight: 800,
                                            cursor: "pointer",
                                        }, children: "View Doctor Profile" })] }))] })] })] }));
}
function TopStatCard({ title, value, tone, }) {
    const styles = tone === "dark"
        ? { bg: "#17212f", color: "#ffffff", sub: "#cbd5e1" }
        : tone === "green"
            ? { bg: "#eaffd0", color: "#1f2937", sub: "#4b5563" }
            : tone === "blue"
                ? { bg: "#dff4ff", color: "#1f2937", sub: "#4b5563" }
                : { bg: "#f8fafc", color: "#1f2937", sub: "#64748b" };
    return (_jsxs("div", { style: {
            background: styles.bg,
            color: styles.color,
            borderRadius: 22,
            padding: 20,
            minHeight: 120,
            boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
        }, children: [_jsx("div", { style: { color: styles.sub, marginBottom: 18 }, children: title }), _jsx("div", { style: { fontSize: 34, fontWeight: 800 }, children: value })] }));
}
function InfoRow({ label, value }) {
    return (_jsxs("div", { style: {
            display: "flex",
            justifyContent: "space-between",
            gap: 14,
            borderBottom: "1px solid #f1f5f9",
            paddingBottom: 8,
        }, children: [_jsx("div", { style: { color: "#64748b" }, children: label }), _jsx("div", { style: { fontWeight: 700, textAlign: "right" }, children: value })] }));
}
