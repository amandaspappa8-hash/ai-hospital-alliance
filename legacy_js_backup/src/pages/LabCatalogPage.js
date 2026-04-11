import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import { Beaker, Microscope, Dna } from "lucide-react";
import SectionIconBadge from "@/components/app/SectionIconBadge";
const ordersSeed = [
    {
        id: "LAB-1001",
        patient: "Ali Hassan",
        test: "CBC",
        category: "Hematology",
        status: "Completed",
        sample: "Blood",
        time: "08:20",
        result: "WBC 7.2, Hb 13.8, Platelets 240",
    },
    {
        id: "LAB-1002",
        patient: "Sara Omar",
        test: "CRP",
        category: "Inflammation",
        status: "Abnormal",
        sample: "Blood",
        time: "09:05",
        result: "CRP 48 mg/L",
    },
    {
        id: "LAB-1003",
        patient: "Mohamed Salem",
        test: "Creatinine",
        category: "Renal",
        status: "Processing",
        sample: "Blood",
        time: "09:40",
    },
    {
        id: "LAB-1004",
        patient: "Lina Kareem",
        test: "Urinalysis",
        category: "Urine",
        status: "Pending",
        sample: "Urine",
        time: "10:10",
    },
];
const classicalTests = [
    "CBC",
    "ESR",
    "CRP",
    "Glucose",
    "Urea",
    "Creatinine",
    "LFT",
    "Urinalysis",
    "Electrolytes",
    "HbA1c",
    "Lipid Profile",
    "Blood Group",
];
const specializedTests = [
    "Hormonal Panel",
    "Immunology",
    "Microbiology",
    "Culture & Sensitivity",
    "Cardiac Markers",
    "Autoimmune Panel",
    "Coagulation Tests",
    "Endocrine Tests",
    "Drug Monitoring",
    "Vitamin D",
    "Ferritin",
    "Thyroid Profile",
];
const geneticsTests = [
    "Tumor Markers",
    "PCR",
    "DNA Analysis",
    "Genetic Screening",
    "Cytogenetics",
    "Molecular Pathology",
    "Nuclear Markers",
    "Oncology Panels",
    "Gene Mutation Testing",
    "BRCA Testing",
    "Viral Load PCR",
    "Chromosomal Analysis",
];
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
            }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", gap: 12 }, children: [_jsx("div", { style: { fontSize: 15, color: "#64748b", fontWeight: 600 }, children: title }), _jsx("div", { style: {
                                width: 44,
                                height: 44,
                                borderRadius: 16,
                                background: "rgba(255,255,255,0.45)",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                color: "#334155",
                            }, children: icon })] }), _jsx("div", { style: { fontSize: 56, fontWeight: 700, lineHeight: 1, color: "#334155" }, children: value })] }) }));
}
export default function LabCatalogPage() {
    const [query, setQuery] = useState("");
    const [selectedOrderId, setSelectedOrderId] = useState("LAB-1002");
    const [selectedSection, setSelectedSection] = useState("classical");
    const [selectedTests, setSelectedTests] = useState([]);
    const [interpretation, setInterpretation] = useState("Inflammatory marker is elevated. Clinical correlation is recommended.");
    const filteredOrders = useMemo(() => {
        const q = query.trim().toLowerCase();
        if (!q)
            return ordersSeed;
        return ordersSeed.filter((order) => order.id.toLowerCase().includes(q) ||
            order.patient.toLowerCase().includes(q) ||
            order.test.toLowerCase().includes(q) ||
            order.category.toLowerCase().includes(q));
    }, [query]);
    const selectedOrder = filteredOrders.find((o) => o.id === selectedOrderId) ??
        ordersSeed.find((o) => o.id === selectedOrderId) ??
        ordersSeed[0];
    function toggleTest(testName) {
        setSelectedTests((prev) => prev.includes(testName)
            ? prev.filter((item) => item !== testName)
            : [...prev, testName]);
    }
    function renderTestList(title, tests) {
        return (_jsxs("div", { className: "rounded-3xl border border-green-200 bg-white/95 p-6 shadow-sm", children: [_jsxs("div", { className: "mb-4", children: [_jsx("h2", { className: "text-2xl font-bold text-slate-700", children: title }), _jsx("p", { className: "text-sm text-slate-500 mt-2", children: "\u0627\u062E\u062A\u0631 \u0627\u0644\u062A\u062D\u0627\u0644\u064A\u0644 \u0627\u0644\u0645\u0637\u0644\u0648\u0628\u0629 \u0645\u0646 \u0627\u0644\u0645\u0631\u0628\u0639\u0627\u062A \u0627\u0644\u062A\u0627\u0644\u064A\u0629" })] }), _jsx("div", { className: "grid gap-3 md:grid-cols-2 xl:grid-cols-3", children: tests.map((test) => {
                        const checked = selectedTests.includes(test);
                        return (_jsxs("label", { className: `flex items-center gap-3 rounded-2xl border p-4 cursor-pointer transition ${checked
                                ? "border-emerald-400 bg-emerald-50 shadow-sm"
                                : "border-slate-200 bg-white hover:border-green-300"}`, children: [_jsx("input", { type: "checkbox", checked: checked, onChange: () => toggleTest(test), className: "h-5 w-5" }), _jsx("span", { className: "font-medium text-slate-700", children: test })] }, test));
                    }) })] }));
    }
    return (_jsxs("div", { style: { padding: "24px", color: "white" }, children: [_jsx("h1", { style: { fontSize: "30px", marginBottom: "8px" }, children: "Laboratory Dashboard" }), _jsx("p", { style: { opacity: 0.8, marginBottom: "20px" }, children: "Orders, specimen workflow, results review, and AI clinical interpretation" }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
                    gap: "16px",
                    marginBottom: "24px",
                }, children: [_jsx("div", { style: { gridColumn: "span 5" }, children: _jsx(OverviewLikeCard, { title: "Classical Lab Tests", value: String(classicalTests.length), selected: selectedSection === "classical", onClick: () => setSelectedSection("classical"), bg: "#d9f2ff", border: "#bfe7fb", icon: _jsx(SectionIconBadge, { icon: _jsx(Microscope, { size: 20, strokeWidth: 2 }), bg: "rgba(6,182,212,0.15)", color: "#0e7490" }) }) }), _jsx("div", { style: { gridColumn: "span 4" }, children: _jsx(OverviewLikeCard, { title: "Specialized Tests", value: String(specializedTests.length), selected: selectedSection === "specialized", onClick: () => setSelectedSection("specialized"), bg: "#d8fbf4", border: "#b8efe4", icon: _jsx(SectionIconBadge, { icon: _jsx(Dna, { size: 20, strokeWidth: 2 }), bg: "rgba(168,85,247,0.15)", color: "#6d28d9" }) }) }), _jsx("div", { style: { gridColumn: "span 3" }, children: _jsx(OverviewLikeCard, { title: "Oncology, DNA & Genetic", value: String(geneticsTests.length), selected: selectedSection === "genetics", onClick: () => setSelectedSection("genetics"), bg: "#f7ecff", border: "#e9d1fb", icon: _jsx(SectionIconBadge, { icon: _jsx(Beaker, { size: 20, strokeWidth: 2 }), bg: "rgba(16,185,129,0.15)", color: "#065f46" }) }) })] }), _jsxs("div", { className: "mb-6", children: [selectedSection === "classical" && renderTestList("Classical Lab Tests", classicalTests), selectedSection === "specialized" && renderTestList("Specialized Tests", specializedTests), selectedSection === "genetics" && renderTestList("Oncology, DNA & Genetic Tests", geneticsTests)] }), _jsxs("div", { className: "grid gap-6 xl:grid-cols-12", children: [_jsxs("div", { className: "xl:col-span-4 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Selected Tests" }), _jsxs("span", { className: "rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700", children: [selectedTests.length, " selected"] })] }), selectedTests.length === 0 ? (_jsx("div", { className: "rounded-2xl border border-dashed border-green-200 bg-green-50 p-4 text-sm text-slate-600", children: "\u0644\u0645 \u064A\u062A\u0645 \u0627\u062E\u062A\u064A\u0627\u0631 \u0623\u064A \u062A\u062D\u0644\u064A\u0644 \u0628\u0639\u062F" })) : (_jsx("div", { className: "space-y-2", children: selectedTests.map((test) => (_jsxs("div", { className: "flex items-center justify-between rounded-xl border border-green-100 bg-green-50 p-3", children: [_jsx("span", { className: "font-medium text-slate-800", children: test }), _jsx("button", { onClick: () => toggleTest(test), className: "rounded-lg bg-white px-2 py-1 text-xs text-rose-600 border border-rose-100", children: "Remove" })] }, test))) })), _jsx("button", { className: "mt-4 w-full rounded-xl bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700", children: "Confirm Lab Request" })] }), _jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Lab Orders Queue" }), _jsx("span", { className: "rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700", children: "Live Queue" })] }), _jsx("input", { value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Search patient, order, test...", className: "w-full rounded-xl border border-green-200 bg-green-50/60 px-4 py-3 outline-none focus:border-emerald-400" }), _jsx("div", { className: "mt-4 space-y-3", children: filteredOrders.map((order) => (_jsxs("button", { onClick: () => setSelectedOrderId(order.id), className: `w-full rounded-2xl border p-4 text-left transition ${selectedOrderId === order.id
                                                ? "border-emerald-400 bg-gradient-to-r from-green-50 to-emerald-50 shadow"
                                                : "border-slate-200 bg-white hover:border-green-300 hover:bg-green-50/40"}`, children: [_jsx("div", { className: "font-semibold text-slate-900", children: order.patient }), _jsxs("div", { className: "mt-1 text-sm text-slate-600", children: [order.test, " \u2022 ", order.category] }), _jsxs("div", { className: "mt-2 text-xs text-slate-500", children: ["Order ID: ", order.id, " \u2022 ", order.sample, " \u2022 ", order.time] }), _jsx("div", { className: "mt-3", children: _jsx("span", { className: `rounded-full px-2.5 py-1 text-[11px] font-semibold ${statusClasses(order.status)}`, children: order.status }) })] }, order.id))) })] })] }), _jsxs("div", { className: "xl:col-span-5 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-white/95 p-5 shadow-sm", children: [_jsxs("div", { className: "mb-4", children: [_jsx("h2", { className: "text-xl font-bold text-green-950", children: "Selected Result" }), _jsx("p", { className: "mt-1 text-sm text-slate-600", children: "Result details, sample status, and validation summary" })] }), _jsxs("div", { className: "rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 via-emerald-50 to-white p-5", children: [_jsxs("div", { className: "grid gap-4 sm:grid-cols-2", children: [_jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Patient" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.patient })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Order ID" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.id })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Test" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.test })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Category" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.category })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Sample" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.sample })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Status" }), _jsx("div", { className: "font-semibold text-green-950", children: selectedOrder.status })] })] }), _jsxs("div", { className: "mt-4 rounded-xl bg-white p-4 border border-emerald-100", children: [_jsx("div", { className: "text-sm text-slate-500", children: "Result Summary" }), _jsx("div", { className: "mt-2 font-medium text-slate-800", children: selectedOrder.result ?? "Result not available yet." })] })] })] }), _jsxs("div", { className: "rounded-2xl border border-emerald-200 bg-gradient-to-br from-white to-green-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Clinical Interpretation" }), _jsx("textarea", { value: interpretation, onChange: (e) => setInterpretation(e.target.value), className: "min-h-[220px] w-full rounded-2xl border border-green-200 bg-white px-4 py-4 outline-none focus:border-emerald-400", placeholder: "Write lab interpretation..." }), _jsxs("div", { className: "mt-4 flex flex-wrap gap-3", children: [_jsx("button", { className: "rounded-xl bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700", children: "Save Interpretation" }), _jsx("button", { className: "rounded-xl bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700", children: "Validate Result" }), _jsx("button", { className: "rounded-xl bg-slate-800 px-4 py-2 font-semibold text-white hover:bg-slate-900", children: "Send to EMR" })] })] })] }), _jsxs("div", { className: "xl:col-span-3 space-y-6", children: [_jsxs("div", { className: "rounded-2xl border border-green-200 bg-gradient-to-br from-green-100 to-white p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Department Load" }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Hematology" }), _jsx("span", { className: "font-bold text-green-950", children: "10" })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Biochemistry" }), _jsx("span", { className: "font-bold text-green-950", children: "8" })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Renal" }), _jsx("span", { className: "font-bold text-green-950", children: "5" })] }), _jsxs("div", { className: "rounded-xl bg-white p-4 border border-green-100 flex items-center justify-between", children: [_jsx("span", { className: "text-slate-700", children: "Inflammation" }), _jsx("span", { className: "font-bold text-green-950", children: "4" })] })] })] }), _jsxs("div", { className: "rounded-2xl border border-lime-200 bg-gradient-to-br from-lime-50 to-green-50 p-5 shadow-sm", children: [_jsx("h2", { className: "text-xl font-bold text-green-950 mb-4", children: "Quick Actions" }), _jsxs("div", { className: "space-y-3", children: [_jsx("button", { className: "w-full rounded-xl bg-green-600 px-4 py-3 text-left font-semibold text-white hover:bg-green-700", children: "+ New Lab Order" }), _jsx("button", { className: "w-full rounded-xl bg-emerald-600 px-4 py-3 text-left font-semibold text-white hover:bg-emerald-700", children: "Open Analyzer Queue" }), _jsx("button", { className: "w-full rounded-xl bg-slate-800 px-4 py-3 text-left font-semibold text-white hover:bg-slate-900", children: "Review Abnormal Results" })] })] })] })] })] }));
}
