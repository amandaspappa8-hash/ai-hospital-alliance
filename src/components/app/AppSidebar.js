import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { NavLink } from "react-router-dom";
import { Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarGroupLabel, SidebarGroupContent, SidebarHeader, SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarRail, SidebarSeparator, } from "@/components/ui/sidebar";
const workspace = [
    { title: "Home", to: "/" },
    { title: "Overview", to: "/overview" },
    { title: "Dashboard", to: "/dashboard" },
];
const clinical = [
    { title: "Patients", to: "/patients" },
    { title: "Appointments", to: "/appointments" },
    { title: "Clinical Notes", to: "/notes" },
];
const orders = [
    { title: "Prescriptions", to: "/prescriptions" },
    { title: "Labs", to: "/labs" },
    { title: "Imaging", to: "/imaging" },
    { title: "CT / MRI", to: "/ct-mri" },
];
const documents = [
    { title: "Files", to: "/files" },
    { title: "Reports", to: "/reports" },
    { title: "PACS / DICOM", to: "/pacs" },
];
const pharmacy = [
    { title: "Formulary", to: "/formulary" },
    { title: "Medications", to: "/medications" },
    { title: "Interactions & Allergies", to: "/interactions" },
];
const system = [
    { title: "Settings", to: "/settings" },
    { title: "Logout", to: "/logout" },
];
function NavSection({ label, items }) {
    return (_jsxs(SidebarGroup, { children: [_jsx(SidebarGroupLabel, { children: label }), _jsx(SidebarGroupContent, { children: _jsx(SidebarMenu, { children: items.map((item) => (_jsx(SidebarMenuItem, { children: _jsx(SidebarMenuButton, { asChild: true, children: _jsx(NavLink, { to: item.to, className: ({ isActive }) => isActive ? "font-medium text-foreground" : "text-muted-foreground", end: true, children: _jsx("span", { children: item.title }) }) }) }, item.to))) }) })] }));
}
export default function AppSidebar() {
    return (_jsxs(Sidebar, { collapsible: "icon", children: [_jsx(SidebarHeader, { className: "px-2", children: _jsxs("div", { className: "flex items-center gap-2 px-2 py-2", children: [_jsx("div", { className: "size-8 rounded-md bg-primary/10" }), _jsxs("div", { className: "flex flex-col leading-tight", children: [_jsx("span", { className: "text-sm font-semibold", children: "AI Hospital Alliance" }), _jsx("span", { className: "text-xs text-muted-foreground", children: "Admin" })] })] }) }), _jsx(SidebarSeparator, {}), _jsxs(SidebarContent, { children: [_jsx(NavSection, { label: "Workspace", items: workspace }), _jsx(NavSection, { label: "Clinical", items: clinical }), _jsx(NavSection, { label: "Orders", items: orders }), _jsx(NavSection, { label: "Documents", items: documents }), _jsx(NavSection, { label: "Pharmacy", items: pharmacy }), _jsx(NavSection, { label: "System", items: system })] }), _jsx(SidebarSeparator, {}), _jsx(SidebarFooter, { className: "p-2", children: _jsx("div", { className: "rounded-md border p-3 text-xs text-muted-foreground", children: "Secure Dev Mode" }) }), _jsx(SidebarRail, {})] }));
}
