import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
export default function DashboardLayout() {
    const location = useLocation();
    return (_jsx("div", { className: "min-h-screen bg-background text-foreground", children: _jsxs("div", { className: "mx-auto flex w-full max-w-[1400px]", children: [_jsx(Sidebar, { currentPath: location.pathname }), _jsxs("main", { className: "min-w-0 flex-1", children: [_jsx(Topbar, {}), _jsx("div", { className: "p-4 md:p-6", children: _jsx(Outlet, {}) })] })] }) }));
}
