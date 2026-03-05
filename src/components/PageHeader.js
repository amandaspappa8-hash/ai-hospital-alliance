import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
export default function PageHeader({ title, subtitle, actions }) {
    return (_jsxs("div", { className: "mb-4 flex items-start justify-between gap-4", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-semibold", children: title }), subtitle && _jsx("p", { className: "text-sm text-muted-foreground", children: subtitle })] }), actions && _jsx("div", { className: "shrink-0", children: actions })] }));
}
