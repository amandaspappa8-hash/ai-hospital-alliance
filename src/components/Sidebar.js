import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { LayoutDashboard, Users, Calendar, FileText, Settings, HeartPulse, } from "lucide-react";
const nav = [
    { to: "/overview", label: "Overview", icon: LayoutDashboard },
    { to: "/patients", label: "Patients", icon: Users, badge: "New" },
    { to: "/appointments", label: "Appointments", icon: Calendar },
    { to: "/reports", label: "Reports", icon: FileText },
    { to: "/settings", label: "Settings", icon: Settings },
];
export default function Sidebar({ currentPath }) {
    return (_jsx("aside", { className: "sticky top-0 hidden h-screen w-[280px] shrink-0 border-r bg-card/30 backdrop-blur md:block", children: _jsxs("div", { className: "flex h-full flex-col", children: [_jsx("div", { className: "p-5", children: _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("div", { className: "flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground", children: _jsx(HeartPulse, { className: "h-5 w-5" }) }), _jsxs("div", { className: "leading-tight", children: [_jsx("div", { className: "font-semibold", children: "AI Hospital Alliance" }), _jsx("div", { className: "text-xs text-muted-foreground", children: "Medical-grade UI" })] })] }) }), _jsx(Separator, {}), _jsx("nav", { className: "flex-1 space-y-1 p-3", children: nav.map((item) => {
                        const active = currentPath === item.to;
                        const Icon = item.icon;
                        return (_jsxs(Link, { to: item.to, className: cn("flex items-center justify-between rounded-xl px-3 py-2 text-sm transition", active
                                ? "bg-primary/10 text-primary"
                                : "text-muted-foreground hover:bg-muted hover:text-foreground"), children: [_jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Icon, { className: "h-4 w-4" }), item.label] }), item.badge ? _jsx(Badge, { variant: "secondary", children: item.badge }) : null] }, item.to));
                    }) }), _jsx("div", { className: "p-4 text-xs text-muted-foreground", children: "v0.1 \u2022 Vite + Tailwind + shadcn/ui" })] }) }));
}
