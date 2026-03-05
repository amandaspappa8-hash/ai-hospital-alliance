import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, Folder, Home, LogIn } from "lucide-react";
import { Separator } from "@/components/ui/separator";
const nav = [
    { to: "/", label: "Home", icon: Home },
    { to: "/overview", label: "Dashboard", icon: LayoutDashboard },
    { to: "/files", label: "File Manager", icon: Folder },
    { to: "/login", label: "Login", icon: LogIn },
];
export default function AppShell({ children }) {
    const { pathname } = useLocation();
    return (_jsx("div", { className: "min-h-screen bg-background", children: _jsxs("div", { className: "flex", children: [_jsxs("aside", { className: "hidden md:flex md:w-72 md:flex-col md:border-r md:bg-muted/20", children: [_jsxs("div", { className: "px-6 py-5", children: [_jsx("div", { className: "text-lg font-semibold", children: "AI Hospital Alliance" }), _jsx("div", { className: "text-xs text-muted-foreground", children: "Admin Console" })] }), _jsx(Separator, {}), _jsx("nav", { className: "p-3 space-y-1", children: nav.map((item) => {
                                const Icon = item.icon;
                                const active = pathname === item.to;
                                return (_jsxs(Link, { to: item.to, className: [
                                        "flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition",
                                        active
                                            ? "bg-muted text-foreground"
                                            : "text-muted-foreground hover:bg-muted/60 hover:text-foreground",
                                    ].join(" "), children: [_jsx(Icon, { className: "h-4 w-4" }), item.label] }, item.to));
                            }) }), _jsx("div", { className: "mt-auto p-4 text-xs text-muted-foreground", children: "v0.1 \u2022 Vite + React + shadcn/ui" })] }), _jsxs("main", { className: "flex-1", children: [_jsx("header", { className: "sticky top-0 z-10 border-b bg-background/80 backdrop-blur", children: _jsxs("div", { className: "mx-auto max-w-6xl px-4 py-3 flex items-center justify-between", children: [_jsx("div", { className: "text-sm text-muted-foreground", children: pathname === "/" ? "Home" : pathname.replace("/", "") }), _jsx("div", { className: "text-xs text-muted-foreground", children: "Local \u2022 Secure Dev Mode" })] }) }), _jsx("div", { className: "mx-auto max-w-6xl px-4 py-6", children: children })] })] }) }));
}
