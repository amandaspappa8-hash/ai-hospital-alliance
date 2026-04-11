import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function App() {
    const drugs = [
        {
            name: "Warfarin 5mg",
            interactions: ["Aspirin", "Ibuprofen"],
            risk: "HIGH",
        },
        {
            name: "Metformin 1000mg",
            interactions: [],
            risk: "SAFE",
        },
    ];
    return (_jsxs("div", { style: { padding: 20, fontFamily: "Arial" }, children: [_jsx("h1", { children: "\uD83D\uDC8A Smart Pharmacy" }), drugs.map((drug, index) => (_jsxs("div", { style: {
                    border: "1px solid #ccc",
                    padding: 10,
                    marginBottom: 10,
                    borderRadius: 10,
                }, children: [_jsx("h3", { children: drug.name }), _jsxs("p", { children: ["Risk:", _jsx("b", { style: { color: drug.risk === "HIGH" ? "red" : "green" }, children: drug.risk })] }), drug.interactions.length > 0 ? (_jsxs("p", { children: ["\u26A0 ", drug.interactions.join(", ")] })) : (_jsx("p", { children: "\u2705 No interactions" }))] }, index)))] }));
}
