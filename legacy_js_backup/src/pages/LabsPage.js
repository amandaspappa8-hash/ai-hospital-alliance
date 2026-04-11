import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
const labTests = [
    "CBC",
    "CRP",
    "ESR",
    "HbA1c",
    "Fasting Blood Sugar",
    "Lipid Profile",
    "Liver Function Test",
    "Kidney Function Test",
    "Troponin",
    "D-Dimer",
    "TSH",
    "Vitamin D",
    "Vitamin B12",
];
export default function LabsPage() {
    const [search, setSearch] = useState("");
    const filtered = labTests.filter((t) => t.toLowerCase().includes(search.toLowerCase()));
    return (_jsxs("div", { style: { maxWidth: 700 }, children: [_jsx("h1", { style: { fontSize: 28, fontWeight: 800, marginBottom: 20 }, children: "Laboratory Orders" }), _jsx("input", { placeholder: "Search lab test...", value: search, onChange: (e) => setSearch(e.target.value), style: {
                    width: "100%",
                    padding: 14,
                    borderRadius: 12,
                    border: "1px solid #334155",
                    background: "#020617",
                    color: "white",
                    marginBottom: 20,
                } }), _jsxs("div", { style: {
                    background: "#020617",
                    border: "1px solid #1e293b",
                    borderRadius: 16,
                    padding: 20,
                }, children: [filtered.map((test) => (_jsx("div", { style: {
                            padding: 12,
                            borderBottom: "1px solid #0f172a",
                            cursor: "pointer",
                        }, children: test }, test))), filtered.length === 0 && (_jsx("div", { style: { opacity: 0.5 }, children: "No tests found" }))] })] }));
}
