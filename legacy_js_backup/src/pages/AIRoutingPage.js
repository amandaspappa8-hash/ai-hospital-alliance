import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
export default function AIRoutingPage() {
    const [text, setText] = useState("chest pain, sweating, nausea, shortness of breath");
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState("");
    const [age, setAge] = useState("58");
    const [gender, setGender] = useState("male");
    const [loadingPatients, setLoadingPatients] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [aiResult, setAiResult] = useState(null);
    useEffect(() => {
        async function loadPatients() {
            setLoadingPatients(true);
            try {
                const data = await apiGet("/patients");
                const rows = Array.isArray(data) ? data : [];
                setPatients(rows);
                if (rows.length > 0) {
                    setSelectedPatientId(rows[0].id);
                }
            }
            catch (err) {
                console.error(err);
                setError("Failed to load patients");
            }
            finally {
                setLoadingPatients(false);
            }
        }
        loadPatients();
    }, []);
    async function runAI() {
        if (!selectedPatientId)
            return;
        setLoading(true);
        setError("");
        setAiResult(null);
        try {
            const res = await apiPost(`/ai/clinical-route-and-create-orders/${selectedPatientId}`, {
                chief_complaint: text,
                symptoms: text.split(",").map((s) => s.trim()).filter(Boolean),
                age: Number(age),
                gender,
            });
            setAiResult(res);
        }
        catch (e) {
            console.error(e);
            setError("Failed to run AI routing");
        }
        finally {
            setLoading(false);
        }
    }
    const route = aiResult?.clinical_route;
    return (_jsxs("div", { style: { padding: 30, color: "white" }, children: [_jsx("h1", { style: { fontSize: 28, marginBottom: 8 }, children: "AI Clinical Routing" }), _jsx("p", { style: { opacity: 0.8, marginBottom: 20 }, children: "AI-powered triage, routing, and order generation" }), _jsxs("div", { style: {
                    background: "#111827",
                    border: "1px solid #374151",
                    borderRadius: 12,
                    padding: 18,
                    maxWidth: 900,
                }, children: [_jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("label", { children: "Select Patient" }), _jsx("select", { value: selectedPatientId, onChange: (e) => setSelectedPatientId(e.target.value), style: inputStyle, disabled: loadingPatients, children: patients.map((p) => (_jsxs("option", { value: p.id, children: [p.name, " (", p.id, ")"] }, p.id))) })] }), _jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("label", { children: "Age" }), _jsx("input", { value: age, onChange: (e) => setAge(e.target.value), style: inputStyle })] }), _jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("label", { children: "Gender" }), _jsx("input", { value: gender, onChange: (e) => setGender(e.target.value), style: inputStyle })] }), _jsxs("div", { style: { marginBottom: 12 }, children: [_jsx("label", { children: "Symptoms / Chief Complaint" }), _jsx("textarea", { value: text, onChange: (e) => setText(e.target.value), style: textareaStyle })] }), _jsx("button", { onClick: runAI, style: buttonStyle, disabled: loading || loadingPatients, children: loading ? "Running..." : "Run AI + Create Orders" })] }), error && (_jsx("div", { style: { color: "#fca5a5", marginTop: 16, marginBottom: 16 }, children: error })), route && (_jsxs("div", { style: {
                    marginTop: 24,
                    maxWidth: 900,
                    display: "grid",
                    gap: 16,
                }, children: [_jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Clinical Route" }), _jsxs("div", { children: [_jsx("strong", { children: "Chief Complaint:" }), " ", route.chief_complaint] }), _jsxs("div", { style: { marginTop: 8 }, children: [_jsx("strong", { children: "Triage Level:" }), " ", route.triage_level] }), _jsxs("div", { style: { marginTop: 8 }, children: [_jsx("strong", { children: "Urgency Score:" }), " ", route.urgency_score] })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Route To" }), route.route_to?.length ? route.route_to.map((item, i) => (_jsx("div", { style: itemStyle, children: item }, i))) : _jsx("div", { style: { opacity: 0.8 }, children: "No routing suggestions." })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Suggested Orders" }), route.suggested_orders?.length ? route.suggested_orders.map((order, i) => (_jsxs("div", { style: cardStyle, children: [_jsx("div", { style: { fontWeight: 700 }, children: order.name }), _jsxs("div", { style: { opacity: 0.8, marginTop: 4 }, children: [order.category, " \u2022 ", order.priority] })] }, i))) : _jsx("div", { style: { opacity: 0.8 }, children: "No suggested orders." })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Red Flags" }), route.red_flags?.length ? route.red_flags.map((item, i) => (_jsx("div", { style: itemStyle, children: item }, i))) : _jsx("div", { style: { opacity: 0.8 }, children: "No red flags." })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Next Actions" }), route.next_actions?.length ? route.next_actions.map((item, i) => (_jsx("div", { style: itemStyle, children: item }, i))) : _jsx("div", { style: { opacity: 0.8 }, children: "No next actions." })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Rationale" }), route.rationale?.length ? route.rationale.map((item, i) => (_jsx("div", { style: itemStyle, children: item }, i))) : _jsx("div", { style: { opacity: 0.8 }, children: "No rationale." })] }), _jsxs("div", { style: panelStyle, children: [_jsx("div", { style: sectionTitle, children: "Created Orders" }), aiResult?.created_orders?.length ? aiResult.created_orders.map((order) => (_jsxs("div", { style: cardStyle, children: [_jsxs("div", { style: { fontWeight: 700 }, children: ["#", order.id, " \u2014 ", order.type] }), _jsxs("div", { style: { opacity: 0.8, marginTop: 4 }, children: [order.department, " \u2022 ", order.status] }), order.note && (_jsx("div", { style: { opacity: 0.75, marginTop: 6 }, children: order.note }))] }, order.id))) : _jsx("div", { style: { opacity: 0.8 }, children: "No orders were created." })] })] }))] }));
}
const inputStyle = {
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
    marginTop: "8px",
};
const textareaStyle = {
    width: "100%",
    minHeight: "140px",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
    marginTop: "10px",
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
const panelStyle = {
    padding: 16,
    borderRadius: 12,
    background: "#111827",
    border: "1px solid #374151",
};
const sectionTitle = {
    fontSize: 18,
    fontWeight: 700,
    marginBottom: 12,
};
const itemStyle = {
    padding: "10px 12px",
    marginBottom: 8,
    borderRadius: 10,
    background: "#0b1220",
    border: "1px solid #374151",
};
const cardStyle = {
    padding: "12px",
    background: "#0b1220",
    border: "1px solid #374151",
    borderRadius: "10px",
    marginBottom: "10px",
};
