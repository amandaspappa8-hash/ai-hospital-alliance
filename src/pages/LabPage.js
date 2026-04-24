import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiGet } from "@/lib/api";
export default function LabPage() {
    const { patientId } = useParams();
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        apiGet(`/labs/orders/${patientId}`)
            .then(d => setOrders(Array.isArray(d) ? d : []))
            .catch(() => setOrders([]))
            .finally(() => setLoading(false));
    }, [patientId]);
    return (_jsx("div", { style: { minHeight: "100vh", background: "linear-gradient(135deg,#020817,#0f1629)", padding: "28px 32px", fontFamily: "Inter,Arial,sans-serif", color: "white" }, children: _jsxs("div", { style: { maxWidth: 1000, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx("div", { style: { fontSize: 12, color: "#10b981", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 LABORATORY" }), _jsxs("h1", { style: { margin: 0, fontSize: 26, fontWeight: 900, color: "white" }, children: ["\uD83E\uDDEC Lab Orders \u2014 ", patientId] })] }), _jsx("div", { style: { background: "linear-gradient(135deg,#0f172a,#1a2540)", border: "1px solid rgba(16,185,129,0.2)", borderRadius: 20, padding: 22 }, children: loading ? _jsx("div", { style: { color: "#64748b" }, children: "Loading..." }) : orders.length === 0 ? (_jsxs("div", { style: { color: "#64748b" }, children: ["No lab orders for ", patientId] })) : orders.map((o, i) => (_jsxs("div", { style: { padding: "14px 16px", borderRadius: 12, marginBottom: 10, background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)" }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", marginBottom: 8 }, children: [_jsx("span", { style: { fontWeight: 800, color: "white" }, children: o.id }), _jsx("span", { style: { padding: "2px 10px", borderRadius: 20, fontSize: 11, fontWeight: 700, background: "rgba(16,185,129,0.15)", color: "#4ade80" }, children: o.status })] }), _jsxs("div", { style: { color: "#94a3b8", fontSize: 13 }, children: [o.section, " \u00B7 ", (o.tests ?? []).join(", ")] }), o.result && _jsxs("div", { style: { color: "#4ade80", fontSize: 12, marginTop: 6 }, children: ["Result: ", o.result] })] }, i))) })] }) }));
}
