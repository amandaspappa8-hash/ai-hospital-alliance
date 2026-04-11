import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function DecisionEngineCard({ result }) {
    return (_jsxs("div", { style: cardStyle, children: [_jsx("h3", { style: titleStyle, children: "Smart Decision Engine" }), _jsxs("div", { children: [_jsx("b", { children: "Risk Level:" }), " ", result.riskLevel] }), _jsxs("div", { style: { marginTop: 8 }, children: [_jsx("b", { children: "Impression:" }), " ", result.impression] }), _jsx("div", { style: { marginTop: 8 }, children: _jsx("b", { children: "Plan:" }) }), _jsx("ul", { children: result.plan.map((item) => (_jsx("li", { children: item }, item))) }), _jsxs("div", { style: { marginTop: 8 }, children: [_jsx("b", { children: "Next Step:" }), " ", result.nextStep] })] }));
}
const cardStyle = {
    background: "#111827",
    border: "1px solid #374151",
    borderRadius: 12,
    padding: 16,
    color: "white",
};
const titleStyle = {
    fontSize: 20,
    fontWeight: 700,
    marginBottom: 12,
};
