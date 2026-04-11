import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
export default function OrdersPage() {
    const [patientId, setPatientId] = useState("P-1001");
    const [department, setDepartment] = useState("Lab");
    const [orderType, setOrderType] = useState("Clinical Chemistry");
    const [note, setNote] = useState("AI suggested order");
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [bulkSaving, setBulkSaving] = useState(false);
    const [error, setError] = useState("");
    const [aiDraft, setAiDraft] = useState(null);
    async function loadOrders(pid) {
        setLoading(true);
        setError("");
        try {
            const data = await apiGet(`/orders/${pid}`);
            setOrders(Array.isArray(data) ? data : []);
        }
        catch (err) {
            console.error(err);
            setError("Failed to load orders");
            setOrders([]);
        }
        finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        loadOrders(patientId);
    }, [patientId]);
    useEffect(() => {
        const draft = localStorage.getItem("AI_ORDER_DRAFT");
        if (draft) {
            try {
                const data = JSON.parse(draft);
                setAiDraft(data);
                if (data.patientId) {
                    setPatientId(data.patientId);
                }
                if (data.labs && data.labs.length > 0) {
                    setDepartment("Lab");
                    setOrderType(data.labs[0]);
                    setNote("AI suggested lab order");
                }
                else if (data.drugs && data.drugs.length > 0) {
                    setDepartment("Pharmacy");
                    setOrderType(data.drugs[0]);
                    setNote("AI suggested medication");
                }
                else if (data.routing && data.routing.length > 0) {
                    setDepartment(data.routing[0]);
                    setOrderType("Referral");
                    setNote("AI suggested referral");
                }
            }
            catch (e) {
                console.error("Invalid AI order draft", e);
            }
            finally {
                localStorage.removeItem("AI_ORDER_DRAFT");
            }
        }
    }, []);
    async function createOrder() {
        setSaving(true);
        setError("");
        try {
            await apiPost(`/orders/${patientId}`, {
                type: orderType,
                department,
                note,
            });
            await loadOrders(patientId);
            setNote("");
        }
        catch (err) {
            console.error(err);
            setError("Failed to create order");
        }
        finally {
            setSaving(false);
        }
    }
    async function createAllAiOrders() {
        if (!aiDraft)
            return;
        setBulkSaving(true);
        setError("");
        try {
            const tasks = [];
            for (const lab of aiDraft.labs ?? []) {
                tasks.push(apiPost(`/orders/${patientId}`, {
                    type: lab,
                    department: "Lab",
                    note: "AI suggested lab order",
                }));
            }
            for (const drug of aiDraft.drugs ?? []) {
                tasks.push(apiPost(`/orders/${patientId}`, {
                    type: drug,
                    department: "Pharmacy",
                    note: "AI suggested medication order",
                }));
            }
            for (const route of aiDraft.routing ?? []) {
                tasks.push(apiPost(`/orders/${patientId}`, {
                    type: "Referral",
                    department: route,
                    note: "AI suggested referral",
                }));
            }
            await Promise.all(tasks);
            await loadOrders(patientId);
            setAiDraft(null);
            alert("All AI orders created successfully");
        }
        catch (err) {
            console.error(err);
            setError("Failed to create AI orders");
        }
        finally {
            setBulkSaving(false);
        }
    }
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Orders Engine" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Clinical workflow orders for labs, imaging, pharmacy, and referrals" }), aiDraft && (_jsxs("div", { style: {
                    background: "#0f172a",
                    border: "1px solid #38bdf8",
                    borderRadius: "12px",
                    padding: "18px",
                    maxWidth: "760px",
                    marginBottom: "20px",
                }, children: [_jsx("div", { style: { fontSize: "20px", fontWeight: 700, marginBottom: "12px" }, children: "AI Order Draft" }), _jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Patient:" }), " ", aiDraft.patientName ?? "Unknown", " (", patientId, ")"] }), _jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Age:" }), " ", aiDraft.patientAge ?? "N/A", " | ", _jsx("strong", { children: "Gender:" }), " ", aiDraft.patientGender ?? "N/A"] }), _jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Severity:" }), " ", aiDraft.severity ?? "N/A", " | ", _jsx("strong", { children: "Risk:" }), " ", aiDraft.riskScore ?? "N/A", "/100"] }), aiDraft.actions && aiDraft.actions.length > 0 && (_jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Recommended Actions:" }), " ", aiDraft.actions.join(" | ")] })), aiDraft.routing && aiDraft.routing.length > 0 && (_jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Routing:" }), " ", aiDraft.routing.join(", ")] })), aiDraft.labs && aiDraft.labs.length > 0 && (_jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Suggested Labs:" }), " ", aiDraft.labs.join(", ")] })), aiDraft.drugs && aiDraft.drugs.length > 0 && (_jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Suggested Medications:" }), " ", aiDraft.drugs.join(", ")] })), aiDraft.alerts && aiDraft.alerts.length > 0 && (_jsxs("div", { style: { marginBottom: "10px" }, children: [_jsx("strong", { children: "Alerts:" }), " ", aiDraft.alerts.join(" | ")] })), _jsx("button", { onClick: createAllAiOrders, style: {
                            marginTop: "12px",
                            padding: "12px 18px",
                            borderRadius: "10px",
                            border: "1px solid #38bdf8",
                            background: "#0284c7",
                            color: "white",
                            cursor: "pointer",
                            fontWeight: 700,
                        }, children: bulkSaving ? "Creating AI Orders..." : "Create All AI Orders" })] })), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #374151",
                    borderRadius: "12px",
                    padding: "18px",
                    maxWidth: "640px",
                    marginBottom: "20px",
                }, children: [_jsxs("div", { style: { marginBottom: "12px" }, children: [_jsx("label", { children: "Patient ID" }), _jsx("input", { value: patientId, onChange: (e) => setPatientId(e.target.value), style: inputStyle })] }), _jsxs("div", { style: { marginBottom: "12px" }, children: [_jsx("label", { children: "Department" }), _jsxs("select", { value: department, onChange: (e) => setDepartment(e.target.value), style: inputStyle, children: [_jsx("option", { value: "Lab", children: "Lab" }), _jsx("option", { value: "Radiology", children: "Radiology" }), _jsx("option", { value: "Emergency", children: "Emergency" }), _jsx("option", { value: "Cardiology", children: "Cardiology" }), _jsx("option", { value: "Internal Medicine", children: "Internal Medicine" }), _jsx("option", { value: "Pharmacy", children: "Pharmacy" })] })] }), _jsxs("div", { style: { marginBottom: "12px" }, children: [_jsx("label", { children: "Order Type" }), _jsx("input", { value: orderType, onChange: (e) => setOrderType(e.target.value), style: inputStyle })] }), _jsxs("div", { style: { marginBottom: "12px" }, children: [_jsx("label", { children: "Note" }), _jsx("textarea", { value: note, onChange: (e) => setNote(e.target.value), style: textareaStyle })] }), _jsx("button", { onClick: createOrder, style: buttonStyle, children: saving ? "Creating..." : "Create Order" })] }), error && _jsx("div", { style: { color: "#fca5a5", marginBottom: "16px" }, children: error }), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #374151",
                    borderRadius: "12px",
                    padding: "18px",
                    maxWidth: "760px",
                }, children: [_jsx("div", { style: { fontSize: "20px", fontWeight: 700, marginBottom: "12px" }, children: "Patient Orders" }), loading ? (_jsx("div", { children: "Loading..." })) : orders.length === 0 ? (_jsx("div", { style: { opacity: 0.8 }, children: "No orders for this patient." })) : (_jsx("div", { style: { display: "grid", gap: "10px" }, children: orders.map((order) => (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { fontWeight: 700 }, children: ["#", order.id, " \u2014 ", order.type] }), _jsxs("div", { style: { opacity: 0.82, marginTop: "4px" }, children: [order.department, " \u2022 ", order.status] }), order.note && (_jsx("div", { style: { opacity: 0.75, marginTop: "6px" }, children: order.note }))] }, order.id))) }))] })] }));
}
const inputStyle = {
    width: "100%",
    marginTop: "6px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const textareaStyle = {
    width: "100%",
    minHeight: "100px",
    marginTop: "6px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
const buttonStyle = {
    padding: "12px 18px",
    borderRadius: "10px",
    border: "1px solid #22c55e",
    background: "#166534",
    color: "white",
    cursor: "pointer",
    fontWeight: 600,
};
const cardStyle = {
    padding: "12px",
    background: "#0b1220",
    border: "1px solid #374151",
    borderRadius: "10px",
};
