import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Outlet } from "react-router-dom";
export default function PublicLayout() {
    return (_jsxs("div", { className: "min-h-screen bg-background text-foreground", children: [_jsx("header", { className: "border-b", children: _jsxs("div", { className: "mx-auto max-w-6xl px-4 py-4 flex items-center justify-between", children: [_jsx("div", { className: "font-semibold", children: "AI Hospital Alliance" }), _jsx("nav", { className: "text-sm text-muted-foreground", children: "Public" })] }) }), _jsx("main", { className: "mx-auto max-w-6xl px-4 py-10", children: _jsx(Outlet, {}) })] }));
}
