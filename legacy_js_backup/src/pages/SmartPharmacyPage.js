import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useMemo, useState } from "react";
import "../styles/medical-ui.css";
import { drugCatalog } from "../data/drugCatalog";
export default function SmartPharmacyPage() {
    const [query, setQuery] = useState("");
    const filtered = useMemo(() => {
        const q = query.trim().toLowerCase();
        if (!q)
            return drugCatalog;
        return drugCatalog.filter((d) => d.name.toLowerCase().includes(q) ||
            d.category.toLowerCase().includes(q) ||
            d.form.toLowerCase().includes(q));
    }, [query]);
    const selected = filtered[0] ?? null;
    return (_jsxs("div", { children: [_jsx("h1", { className: "page-title", children: "Smart Pharmacy" }), _jsxs("div", { style: {
                    display: "grid",
                    gridTemplateColumns: "380px minmax(0,1fr)",
                    gap: 20,
                    alignItems: "start",
                }, children: [_jsxs("div", { className: "med-card", children: [_jsx("div", { style: { fontWeight: 700, marginBottom: 10 }, children: "Drug Search" }), _jsx("input", { placeholder: "Type drug name...", value: query, onChange: (e) => setQuery(e.target.value), style: {
                                    width: "100%",
                                    padding: 12,
                                    borderRadius: 10,
                                    border: "1px solid #334155",
                                    background: "#020617",
                                    color: "white",
                                    marginBottom: 14,
                                } }), _jsx("div", { style: { display: "grid", gap: 10 }, children: filtered.map((drug) => (_jsxs("div", { style: {
                                        padding: 12,
                                        borderRadius: 10,
                                        background: "#0b1220",
                                        border: "1px solid #1f2937",
                                    }, children: [_jsx("div", { style: { fontWeight: 700 }, children: drug.name }), _jsx("div", { style: { opacity: 0.7, fontSize: 13 }, children: drug.category })] }, drug.name))) })] }), _jsx("div", { className: "med-card", children: !selected ? (_jsx("div", { style: { opacity: 0.7 }, children: "Select or search a drug to view details." })) : (_jsxs(_Fragment, { children: [_jsx("div", { style: { fontSize: 24, fontWeight: 800, marginBottom: 8 }, children: selected.name }), _jsx("div", { style: { color: "#93c5fd", marginBottom: 18 }, children: selected.category }), _jsxs("div", { className: "med-grid", children: [_jsxs("div", { className: "med-card", children: [_jsx("div", { style: { opacity: 0.7 }, children: "Form" }), _jsx("div", { style: { marginTop: 8, fontWeight: 700 }, children: selected.form })] }), _jsxs("div", { className: "med-card", children: [_jsx("div", { style: { opacity: 0.7 }, children: "Adult Dose" }), _jsx("div", { style: { marginTop: 8, fontWeight: 700 }, children: selected.adultDose })] }), _jsxs("div", { className: "med-card", children: [_jsx("div", { style: { opacity: 0.7 }, children: "Pediatric Dose" }), _jsx("div", { style: { marginTop: 8, fontWeight: 700 }, children: selected.pediatricDose })] }), _jsxs("div", { className: "med-card", children: [_jsx("div", { style: { opacity: 0.7 }, children: "Frequency" }), _jsx("div", { style: { marginTop: 8, fontWeight: 700 }, children: selected.frequency })] }), _jsxs("div", { className: "med-card", children: [_jsx("div", { style: { opacity: 0.7 }, children: "Max Dose" }), _jsx("div", { style: { marginTop: 8, fontWeight: 700 }, children: selected.maxDose })] })] }), _jsxs("div", { style: { marginTop: 20 }, className: "med-card", children: [_jsx("div", { style: { fontSize: 18, fontWeight: 700, marginBottom: 10 }, children: "Warnings" }), selected.warnings.map((item, i) => (_jsxs("div", { style: { marginBottom: 8 }, children: ["\u2022 ", item] }, i)))] }), _jsxs("div", { style: { marginTop: 20 }, className: "med-card", children: [_jsx("div", { style: { fontSize: 18, fontWeight: 700, marginBottom: 10 }, children: "Clinical Notes" }), selected.notes.map((item, i) => (_jsxs("div", { style: { marginBottom: 8 }, children: ["\u2022 ", item] }, i)))] })] })) })] })] }));
}
