import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
// src/layouts/AppLayout.tsx
import { Outlet } from "react-router-dom";
import AppSidebar from "@/components/app/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
export default function AppLayout() {
    return (_jsxs(SidebarProvider, { children: [_jsx(AppSidebar, {}), _jsx(SidebarInset, { children: _jsx("main", { className: "min-h-screen p-6", children: _jsx(Outlet, {}) }) })] }));
}
