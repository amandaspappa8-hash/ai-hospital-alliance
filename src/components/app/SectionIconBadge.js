import { jsx as _jsx } from "react/jsx-runtime";
export default function SectionIconBadge({ icon, bg = "rgba(255,255,255,0.45)", color = "#334155", size = 46, }) {
    return (_jsx("div", { style: {
            width: size,
            height: size,
            borderRadius: 16,
            background: bg,
            color,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
        }, children: icon }));
}
