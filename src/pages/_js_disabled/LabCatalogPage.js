import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import { Beaker, Microscope, Dna } from "lucide-react";
import SectionIconBadge from "@/components/app/SectionIconBadge";
import { apiGet, apiPost } from "@/lib/api";
function statusClasses(status) {
    switch (status) {
        case "Completed":
            return "bg-emerald-100 text-emerald-700 border border-emerald-200";
        case "Processing":
            return "bg-lime-100 text-lime-700 border border-lime-200";
        case "Pending":
            return "bg-green-100 text-green-700 border border-green-200";
        case "Abnormal":
            return "bg-rose-100 text-rose-700 border border-rose-200";
        default:
            return "bg-slate-100 text-slate-700 border border-slate-200";
    }
}
function OverviewLikeCard({ title, value, selected, onClick, bg, border, icon, }) {
    return (_jsx("button", { onClick: onClick, style: { textAlign: "left", width: "100%" }, children: _jsxs("div", { style: {
                background: bg,
                border: selected ? "2px solid #93c5fd" : `1px solid ${border}`,
                borderRadius: "28px",
                padding: "22px",
                minHeight: "170px",
                boxShadow: "0 8px 24px rgba(15,23,42,0.10)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                transition: "all 0.2s ease",
            }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", gap: 12 }, children: [_jsx("div", { style: { fontSize: 15, color: "#64748b", fontWeight: 600 }, children: title }), icon] }), _jsx("div", { style: { fontSize: 56, fontWeight: 700, lineHeight: 1, color: "#334155" }, children: value })] }) }));
}
export default function LabCatalogPage() {
    const [query, setQuery] = useState("");
    const [selectedOrderId, setSelectedOrderId] = useState("");
    const [selectedSection, setSelectedSection] = useState("classical");
    const [selectedTests, setSelectedTests] = useState([]);
    const [interpretation, setInterpretation] = useState("Inflammatory marker is elevated. Clinical correlation is recommended.");
    const [resultText, setResultText] = useState("");
    const [catalog, setCatalog] = useState({
        classical: [],
        specialized: [],
        genetics: [],
    });
    const [patients, setPatients] = useState([]);
    const [selectedPatientId, setSelectedPatientId] = useState("");
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [savingResult, setSavingResult] = useState(false);
    const [error, setError] = useState("");
    const selectedPatient = patients.find((p) => p.id === selectedPatientId) ?? patients[0];
    async function loadBaseData() {
        try {
            setLoading(true);
            setError("");
            const [catalogData, patientsData] = await Promise.all([
                apiGet("/labs/catalog"),
                apiGet("/patients"),
            ]);
            setCatalog(catalogData);
            setPatients(Array.isArray(patientsData) ? patientsData : []);
            if (Array.isArray(patientsData) && patientsData.length > 0) {
                setSelectedPatientId((current) => current || patientsData[0].id);
            }
        }
        catch (err) {
            console.error(err);
            setError("Failed to load laboratory base data");
        }
        finally {
            setLoading(false);
        }
    }
    async function loadPatientOrders(patientId) {
        try {
            const ordersData = await apiGet(`/labs/orders/${patientId}`);
            setOrders(Array.isArray(ordersData) ? ordersData : []);
            if (Array.isArray(ordersData) && ordersData.length > 0) {
                setSelectedOrderId(ordersData[0].id);
            }
            else {
                setSelectedOrderId("");
                setResultText("");
            }
        }
        catch (err) {
            console.error(err);
            setError("Failed to load patient lab orders");
        }
    }
    useEffect(() => {
        loadBaseData();
    }, []);
    useEffect(() => {
        if (selectedPatientId) {
            loadPatientOrders(selectedPatientId);
        }
    }, [selectedPatientId]);
    const classicalTests = catalog.classical ?? [];
    const specializedTests = catalog.specialized ?? [];
    const geneticsTests = catalog.genetics ?? [];
    const filteredOrders = useMemo(() => {
        const q = query.trim().toLowerCase();
        if (!q)
            return orders;
        return orders.filter((order) => order.id.toLowerCase().includes(q) ||
            order.patientId.toLowerCase().includes(q) ||
            order.patientName.toLowerCase().includes(q) ||
            order.tests.join(" ").toLowerCase().includes(q) ||
            order.section.toLowerCase().includes(q));
    }, [orders, query]);
    const selectedOrder = filteredOrders.find((o) => o.id === selectedOrderId) ??
        orders.find((o) => o.id === selectedOrderId) ??
        orders[0];
    useEffect(() => {
        setResultText(selectedOrder?.result ?? "");
    }, [selectedOrderId, selectedOrder?.result]);
    function toggleTest(testName) {
        setSelectedTests((prev) => prev.includes(testName)
            ? prev.filter((item) => item !== testName)
            : [...prev, testName]);
    }
    async function createLabOrder() {
        if (!selectedPatient) {
            setError("Select a patient first");
            return;
        }
        if (selectedTests.length === 0) {
            setError("Select at least one test before creating a lab order");
            return;
        }
        try {
            setSaving(true);
            setError("");
            const created = await apiPost("/labs/orders", {
                patientId: selectedPatient.id,
                patientName: selectedPatient.name,
                section: selectedSection,
                tests: selectedTests,
                priority: "Urgent",
            });
            setOrders((prev) => [created, ...prev]);
            setSelectedOrderId(created.id);
            setSelectedTests([]);
        }
        catch (err) {
            console.error(err);
            setError("Failed to create lab order");
        }
        finally {
            setSaving(false);
        }
    }
    async function saveLabResult() {
        if (!selectedOrder) {
            setError("Select a lab order first");
            return;
        }
        if (!resultText.trim()) {
            setError("Write a result before saving");
            return;
        }
        try {
            setSavingResult(true);
            setError("");
            const updated = await apiPost(`/labs/results/${selectedOrder.id}`, {
                result: resultText.trim(),
                status: "Completed",
            });
            setOrders((prev) => prev.map((order) => (order.id === updated.id ? updated : order)));
            setSelectedOrderId(updated.id);
        }
        catch (err) {
            console.error(err);
            setError("Failed to save lab result");
        }
        finally {
            setSavingResult(false);
        }
    }
    function renderTestList(title, tests) {
        return (_jsxs("div", { className: "rounded-3xl border border-green-200 bg-white/95 p-6 shadow-sm", children: [_jsxs("div", { className: "mb-4", children: [_jsx("h2", { className: "text-2xl font-bold text-slate-700", children: title }), _jsx("p", { className: "text-sm text-slate-500 mt-2", children: "\u0627\u062E\u062A\u0631 \u0627\u0644\u062A\u062D\u0627\u0644\u064A\u0644 \u0627\u0644\u0645\u0637\u0644\u0648\u0628\u0629 \u0645\u0646 \u0627\u0644\u0645\u0631\u0628\u0639\u0627\u062A \u0627\u0644\u062A\u0627\u0644\u064A\u0629" })] }), _jsx("div", { className: "grid gap-3 md:grid-cols-2 xl:grid-cols-3", children: tests.map((test) => {
                        const checked = selectedTests.includes(test);
                        return (_jsxs("label", { className: `flex items-center gap-3 rounded-2xl border p-4 cursor-pointer transition ${checked
                                ? "border-emerald-400 bg-emerald-50 shadow-sm"
                                : "border-slate-200 bg-white hover:border-green-300"}`, children: [_jsx("input", { type: "checkbox", checked: checked, onChange: () => toggleTest(test), className: "h-5 w-5" }), _jsx("span", { className: "font-medium text-slate-700", children: test })] }, test));
                    }) })] }));
    }
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Laboratory Dashboard" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Orders, specimen workflow, results review, and AI clinical interpretation" }), error && _jsx("div", { style: { color: "#fca5a5", marginBottom: "16px" }, children: error }), _jsxs("div", { style: {
                    background: "#ffffff",
                    border: "1px solid #d1fae5",
                    borderRadius: "20px",
                    padding: "16px",
                    marginBottom: "24px",
                    color: "#0f172a",
                    display: "grid",
                    gap: "12px",
                }, children: [_jsx("div", { style: { fontWeight: 700, color: "#166534" }, children: "Patient Selection" }), _jsx("select", { value: selectedPatientId, onChange: (e) => setSelectedPatientId(e.target.value), style: {
                            border: "1px solid #bbf7d0",
                            borderRadius: "12px",
                            padding: "12px 14px",
                            background: "#f0fdf4",
                            color: "#0f172a",
                        }, children: patients.map((patient) => (_jsxs("option", { value: patient.id, children: [patient.name, " (", patient.id, ")"] }, patient.id))) })] }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
                    gap: "16px",
                    marginBottom: "24px",
                }, children: [_jsx("div", { style: { gridColumn: "span 5" }, children: _jsx(OverviewLikeCard, { title: "Classical Lab Tests", value: loading ? "..." : String(classicalTests.length), selected: selectedSection === "classical", onClick: () => setSelectedSection("classical"), bg: "#d9f2ff", border: "#bfe7fb", icon: _jsx(SectionIconBadge, { icon: _jsx(Beaker, { size: 20, strokeWidth: 2 }), bg: "rgba(16,185,129,0.15)", color: "#065f46" }) }) }), _jsx("div", { style: { gridColumn: "span 4" }, children: _jsx(OverviewLikeCard, { title: "Specialized Tests", value: loading ? "..." : String(specializedTests.length), selected: selectedSection === "specialized", onClick: () => setSelectedSection("specialized"), bg: "#d8fbf4", border: "#b8efe4", icon: _jsx(SectionIconBadge, { icon: _jsx(Microscope, { size: 20, strokeWidth: 2 }), bg: "rgba(6,182,212,0.15)", color: "#0e7490" }) }) }), _jsx("div", { style: { gridColumn: "span 3" }, children: _jsx(OverviewLikeCard, { title: "Oncology, DNA & Genetic", value: loading ? "..." : String(geneticsTests.length), selected: selectedSection === "genetics", onClick: () => setSelectedSection("genetics"), bg: "#f7ecff", border: "#e9d1fb", icon: _jsx(SectionIconBadge, { icon: _jsx(Dna, { size: 20, strokeWidth: 2 }), bg: "rgba(168,85,247,0.15)", color: "#6d28d9" }) }) })] }), _jsxs("div", { className: "mb-6", children: [selectedSection === "classical" && renderTestList("Classical Lab Tests", classicalTests), selectedSection === "specialized" && renderTestList("Specialized Tests", specializedTests), selectedSection === "genetics" && renderTestList("Oncology, DNA & Genetic Tests", geneticsTests)] }), _jsxs("div", { className: "grid gap-6 xl:grid-cols-12", children: [_jsxs("div", { className: "xl:col-span-4 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Selected Tests" }), _jsxs("span", { className: "rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700", children: [selectedTests.length, " selected"] })] }), selectedTests.length === 0 ? (_jsx("div", { className: "rounded-2xl border border-dashed border-green-200 bg-green-50 p-4 text-sm text-slate-600", children: "\u0644\u0645 \u064A\u062A\u0645 \u0627\u062E\u062A\u064A\u0627\u0631 \u0623\u064A \u062A\u062D\u0644\u064A\u0644 \u0628\u0639\u062F" })) : (_jsx("div", { className: "space-y-2", children: selectedTests.map((test) => (_jsxs("div", { className: "flex items-center justify-between rounded-xl border border-green-100 bg-green-50 p-3", children: [_jsx("span", { className: "font-medium text-slate-800", children: test }), _jsx("button", { onClick: () => toggleTest(test), className: "rounded-lg bg-white px-2 py-1 text-xs text-rose-600 border border-rose-100", children: "Remove" })] }, test))) })), _jsx("button", { onClick: createLabOrder, disabled: saving, className: "mt-4 w-full rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700 disabled:opacity-60", children: saving ? "Creating..." : "Confirm Lab Request" })] }), _jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Lab Orders Queue" }), _jsxs("span", { className: "rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700", children: [filteredOrders.length, " orders"] })] }), _jsx("input", { value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Search patient, order, test...", className: "w-full rounded-xl border border-green-200 bg-green-50/60 px-4 py-3 outline-none focus:border-emerald-400" }), _jsx("div", { className: "mt-4 space-y-3", children: filteredOrders.map((order) => (_jsxs("button", { onClick: () => setSelectedOrderId(order.id), className: `w-full rounded-2xl border p-4 text-left transition ${selectedOrderId === order.id
                                                ? "border-emerald-400 bg-gradient-to-r from-green-50 to-emerald-50 shadow"
                                                : "border-slate-200 bg-white hover:border-green-300 hover:bg-green-50/40"}`, children: [_jsx("div", { className: "font-semibold text-slate-900", children: order.patientName }), _jsx("div", { className: "mt-1 text-sm text-slate-600", children: order.tests.join(", ") }), _jsxs("div", { className: "mt-2 text-xs text-slate-500", children: ["Order ID: ", order.id, " \u2022 ", order.patientId, " \u2022 ", order.section] }), _jsxs("div", { className: "mt-3 flex items-center gap-2", children: [_jsx("span", { className: `rounded-full px-2.5 py-1 text-[11px] font-semibold ${statusClasses(order.status)}`, children: order.status }), _jsx("span", { className: "rounded-full px-2.5 py-1 text-[11px] font-semibold bg-sky-100 text-sky-700 border border-sky-200", children: order.priority })] })] }, order.id))) })] })] }), _jsxs("div", { className: "xl:col-span-5 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Selected Result" }), _jsx("p", { className: "mt-1 text-sm text-slate-600", children: "Result details, sample status, and validation summary" })] }), selectedOrder ? (_jsxs("div", { className: "rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 via-emerald-50 to-white p-5", children: [_jsxs("div", { className: "grid gap-4 sm:grid-cols-2", children: [_jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Patient" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.patientName })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Order ID" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.id })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Tests" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.tests.join(", ") })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Section" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.section })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Priority" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.priority })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Status" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.status })] })] }), _jsxs("div", { className: "mt-4 rounded-xl bg-white p-4 border border-emerald-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Result Summary" }), _jsx("div", { className: "mt-2 font-medium text-slate-800", children: selectedOrder.result?.trim() ? selectedOrder.result : "Result not available yet." })] })] })) : (_jsx("div", { className: "rounded-2xl border border-dashed border-green-200 bg-green-50 p-5 text-slate-600", children: "No order selected." }))] }), _jsxs("div", { className: "rounded-2xl border border-emerald-200 bg-gradient-to-br from-white to-green-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Lab Result Entry" }), _jsx("textarea", { value: resultText, onChange: (e) => setResultText(e.target.value), className: "min-h-[220px] w-full rounded-2xl border border-green-200 bg-white px-4 py-4 outline-none focus:border-emerald-400", placeholder: "Write lab result..." }), _jsxs("div", { className: "mt-4 flex flex-wrap gap-3", children: [_jsx("button", { onClick: saveLabResult, disabled: savingResult || !selectedOrder, className: "rounded-xl bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 disabled:opacity-60", children: savingResult ? "Saving..." : "Save Result" }), _jsx("button", { className: "rounded-xl bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700", children: "Validate Result" }), _jsx("button", { className: "rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900", children: "Send to EMR" })] })] }), _jsxs("div", { className: "rounded-2xl border border-emerald-200 bg-gradient-to-br from-white to-green-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Clinical Interpretation" }), _jsx("textarea", { value: interpretation, onChange: (e) => setInterpretation(e.target.value), className: "min-h-[160px] w-full rounded-2xl border border-green-200 bg-white px-4 py-4 outline-none focus:border-emerald-400", placeholder: "Write lab interpretation..." }), _jsxs("div", { className: "mt-4 flex flex-wrap gap-3", children: [_jsx("button", { className: "rounded-xl bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700", children: "Save Interpretation" }), _jsx("button", { className: "rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900", children: "Review with Physician" })] })] })] }), _jsxs("div", { className: "xl:col-span-3 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 to-white p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Department Load" }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Classical" }), _jsx("span", { className: "font-bold text-green-950", children: classicalTests.length })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Specialized" }), _jsx("span", { className: "font-bold text-green-950", children: specializedTests.length })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Genetics" }), _jsx("span", { className: "font-bold text-green-950", children: geneticsTests.length })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Orders" }), _jsx("span", { className: "font-bold text-green-950", children: orders.length })] })] })] }), _jsxs("div", { className: "rounded-2xl border border-lime-200 bg-gradient-to-br from-lime-50 to-green-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Quick Actions" }), _jsxs("div", { className: "space-y-3", children: [_jsx("button", { onClick: () => selectedPatientId && loadPatientOrders(selectedPatientId), className: "w-full rounded-xl bg-green-600 px-4 py-3 text-left font-semibold text-white hover:bg-green-700", children: "Refresh Patient Orders" }), _jsx("button", { className: "w-full rounded-xl bg-emerald-600 px-4 py-3 text-left font-semibold text-white hover:bg-emerald-700", children: "Open Analyzer Queue" }), _jsx("button", { className: "w-full rounded-xl bg-slate-800 px-4 py-3 text-left font-semibold text-white hover:bg-slate-900", children: "Review Abnormal Results" })] })] })] })] })] }));
}
