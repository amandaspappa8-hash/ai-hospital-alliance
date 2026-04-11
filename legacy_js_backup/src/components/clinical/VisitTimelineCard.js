import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function VisitTimelineCard({ items }) {
    return (_jsxs("div", { style: cardStyle, children: [_jsx("h3", { style: titleStyle, children: "Visit Timeline" }), _jsx("div", { style: { display: "grid", gap: 10 }, children: items.map((item) => (_jsxs("div", { style: itemStyle, children: [_jsx("div", { style: { fontWeight: 700 }, children: item.title }), _jsx("div", { style: { fontSize: 12, opacity: 0.7 }, children: item.time }), _jsx("div", { style: { marginTop: 4 }, children: item.description }), _jsx("div", { style: { marginTop: 4, fontSize: 12, opacity: 0.7 }, children: item.status })] }, item.id))) })] }));
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
const itemStyle = {
    background: "#0b1220",
    border: "1px solid #374151",
    borderRadius: 10,
    padding: 12,
};
