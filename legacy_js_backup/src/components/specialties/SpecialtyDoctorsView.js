import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { getDoctorsBySpecialty } from "@/lib/doctors";
function statusColor(status) {
    if (status === "Available")
        return { bg: "#dcfce7", color: "#166534" };
    if (status === "On Call")
        return { bg: "#fef3c7", color: "#92400e" };
    if (status === "In Surgery")
        return { bg: "#fee2e2", color: "#991b1b" };
    return { bg: "#e5e7eb", color: "#374151" };
}
export default function SpecialtyDoctorsView({ title, icon, description, specialtyName, }) {
    const [doctors, setDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    useEffect(() => {
        async function loadDoctors() {
            try {
                setLoading(true);
                setError("");
                const data = await getDoctorsBySpecialty(specialtyName);
                setDoctors(data);
            }
            catch (err) {
                console.error(err);
                setError(`Failed to load ${specialtyName} doctors`);
                setDoctors([]);
            }
            finally {
                setLoading(false);
            }
        }
        loadDoctors();
    }, [specialtyName]);
    const availableCount = useMemo(() => doctors.filter((d) => d.status === "Available").length, [doctors]);
    const totalPatients = useMemo(() => doctors.reduce((sum, d) => sum + d.patients, 0), [doctors]);
    const avgRating = useMemo(() => {
        if (doctors.length === 0)
            return "0.0";
        return (doctors.reduce((sum, d) => sum + d.rating, 0) / doctors.length).toFixed(1);
    }, [doctors]);
    return (_jsx("div", { style: { padding: 24, color: "#e5eef8" }, children: _jsxs("div", { style: {
                background: "#f8fafc",
                color: "#0f172a",
                borderRadius: 26,
                padding: 24,
                boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
            }, children: [_jsx("div", { style: { fontSize: 44, marginBottom: 12 }, children: icon }), _jsx("div", { style: { fontSize: 32, fontWeight: 800, marginBottom: 10 }, children: title }), _jsx("div", { style: { color: "#64748b", marginBottom: 24 }, children: description }), error && (_jsx("div", { style: { color: "#b91c1c", marginBottom: 16 }, children: error })), _jsxs("div", { style: {
                        display: "grid",
                        gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                        gap: 16,
                        marginBottom: 22,
                    }, children: [_jsx(MiniCard, { title: "Doctors", value: loading ? "..." : String(doctors.length) }), _jsx(MiniCard, { title: "Available Now", value: loading ? "..." : String(availableCount) }), _jsx(MiniCard, { title: "Patients Today", value: loading ? "..." : String(totalPatients) }), _jsx(MiniCard, { title: "Average Rating", value: loading ? "..." : avgRating })] }), _jsxs("div", { style: {
                        background: "white",
                        border: "1px solid #e2e8f0",
                        borderRadius: 22,
                        padding: 18,
                    }, children: [_jsxs("div", { style: { fontSize: 20, fontWeight: 800, marginBottom: 14 }, children: [title, " Doctors"] }), loading ? (_jsx("div", { children: "Loading doctors..." })) : doctors.length === 0 ? (_jsx("div", { children: "No doctors found for this specialty." })) : (_jsx("div", { style: { display: "grid", gap: 12 }, children: doctors.map((doctor) => {
                                const tone = statusColor(doctor.status);
                                return (_jsx("div", { style: {
                                        border: "1px solid #e2e8f0",
                                        background: "#ffffff",
                                        borderRadius: 18,
                                        padding: 16,
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
                                                    .join("") }), _jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800, fontSize: 17 }, children: doctor.name }), _jsxs("div", { style: { color: "#475569", marginTop: 4 }, children: [doctor.specialty, " \u2022 ", doctor.department] }), _jsxs("div", { style: { color: "#64748b", marginTop: 6, fontSize: 13 }, children: ["Experience: ", doctor.experience, " \u2022 Schedule: ", doctor.schedule] }), _jsxs("div", { style: { color: "#64748b", marginTop: 4, fontSize: 13 }, children: ["Phone: ", doctor.phone, " \u2022 Patients today: ", doctor.patients] })] }), _jsxs("div", { style: { textAlign: "right" }, children: [_jsx("div", { style: {
                                                            display: "inline-block",
                                                            background: tone.bg,
                                                            color: tone.color,
                                                            padding: "6px 10px",
                                                            borderRadius: 999,
                                                            fontWeight: 800,
                                                            fontSize: 12,
                                                            marginBottom: 10,
                                                        }, children: doctor.status }), _jsxs("div", { style: { color: "#0f172a", fontWeight: 700 }, children: ["\u2B50 ", doctor.rating] })] })] }) }, doctor.id));
                            }) }))] })] }) }));
}
function MiniCard({ title, value }) {
    return (_jsxs("div", { style: {
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 18,
            padding: 18,
        }, children: [_jsx("div", { style: { color: "#64748b", marginBottom: 10 }, children: title }), _jsx("div", { style: { fontSize: 28, fontWeight: 800 }, children: value })] }));
}
