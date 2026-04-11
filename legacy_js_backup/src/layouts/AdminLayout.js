import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import * as React from "react";
import { useLocation } from "react-router-dom";
import AppSidebar from "@/components/app/AppSidebar";
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { Breadcrumb, BreadcrumbItem, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator, } from "@/components/ui/breadcrumb";
function useCrumbs() {
    const { pathname } = useLocation();
    return pathname.split("/").filter(Boolean);
}
function titleFromPart(part) {
    return part
        .replace(/[-_]/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());
}
export default function AdminLayout({ children, title, subtitle, actions }) {
    const parts = useCrumbs();
    return (_jsxs(SidebarProvider, { children: [_jsx(AppSidebar, {}), _jsxs(SidebarInset, { children: [_jsxs("header", { className: "sticky top-0 z-10 flex h-14 items-center gap-2 border-b bg-background px-4", children: [_jsx(SidebarTrigger, {}), _jsx(Separator, { orientation: "vertical", className: "h-6" }), _jsx(Breadcrumb, { children: _jsxs(BreadcrumbList, { children: [_jsx(BreadcrumbItem, { children: _jsx(BreadcrumbPage, { children: "AI Hospital Alliance" }) }), parts.map((p, i) => (_jsxs(React.Fragment, { children: [_jsx(BreadcrumbSeparator, {}), _jsx(BreadcrumbItem, { children: _jsx(BreadcrumbPage, { children: titleFromPart(p) }) })] }, `${p}-${i}`)))] }) }), _jsx("div", { className: "ml-auto flex items-center gap-2", children: actions })] }), (title || subtitle) && (_jsxs("div", { className: "px-4 pt-4", children: [title && _jsx("h1", { className: "text-2xl font-semibold", children: title }), subtitle && _jsx("p", { className: "text-sm text-muted-foreground", children: subtitle })] })), _jsx("main", { className: "p-4 md:p-6", children: children })] })] }));
}
