import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
import { getUser } from "@/lib/auth-storage";
export default function InteractionsPage() {
    const user = getUser();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const config = {
        MedicationsPage: { title: "Medications", icon: "💊", color: "#f43f5e", endpoint: "/mar/P-1001" },
        InteractionsPage: { title: "Drug Interactions", icon: "⚗️", color: "#a855f7", endpoint: "/drug-intel/interactions/P-1001" },
        LabOrdersPage: { title: "Lab Orders", icon: "🧬", color: "#10b981", endpoint: "/labs/orders" },
        CtMriPage: { title: "CT / MRI Studies", icon: "🖥️", color: "#06b6d4", endpoint: "/radiology/orders" },
    };
    const c = config["InteractionsPage"];
    useEffect(() => {
        apiGet(c.endpoint)
            .then(d => setData(Array.isArray(d) ? d : d?.findings ?? d?.items ?? []))
            .catch(() => setData([]))
            .finally(() => setLoading(false));
    }, []);
    return (_jsx("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: _jsxs("div", { style: { maxWidth: 1100, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx("div", { style: { fontSize: 12, color: c.color, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE" }), _jsxs("h1", { style: { margin: 0, fontSize: 28, fontWeight: 900, background: "linear-gradient(135deg,#fff,#94a3b8)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }, children: [c.icon, " ", c.title] }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: [user?.name, " \u00B7 ", user?.role] })] }), _jsxs("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: `1px solid ${c.color}22`, borderRadius: 20, padding: 24 }, children: [_jsxs("div", { style: { fontWeight: 800, fontSize: 15, color: "white", marginBottom: 18, display: "flex", alignItems: "center", gap: 8 }, children: [_jsx("div", { style: { width: 3, height: 18, background: c.color, borderRadius: 2, boxShadow: `0 0 8px ${c.color}` } }), c.title] }), loading ? (_jsx("div", { style: { color: "#64748b" }, children: "Loading..." })) : data.length === 0 ? (_jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "No data available." })) : (_jsx("div", { style: { display: "flex", flexDirection: "column", gap: 10 }, children: data.map((item, i) => (_jsx("div", { style: { padding: "14px 16px", borderRadius: 12, background: `${c.color}06`, border: `1px solid ${c.color}20` }, children: _jsx("pre", { style: { color: "#cbd5e1", fontSize: 12, margin: 0, whiteSpace: "pre-wrap", fontFamily: "monospace" }, children: JSON.stringify(item, null, 2) }) }, i))) }))] })] }) }));
}
