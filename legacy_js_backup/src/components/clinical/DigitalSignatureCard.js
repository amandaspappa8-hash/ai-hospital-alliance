import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function DigitalSignatureCard({ signature }) {
    return (_jsxs("div", { style: cardStyle, children: [_jsx("h3", { style: titleStyle, children: "Digital Signature" }), _jsx("div", { style: { fontWeight: 700 }, children: signature.doctorName }), _jsx("div", { style: { opacity: 0.8, marginTop: 4 }, children: signature.role }), _jsx("div", { style: { marginTop: 12 }, children: signature.signatureText }), _jsx("div", { style: { marginTop: 8, fontSize: 12, opacity: 0.7 }, children: signature.signedAt })] }));
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
