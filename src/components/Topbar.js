import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Bell, Search } from "lucide-react";
export default function Topbar() {
    return (_jsx("header", { className: "sticky top-0 z-10 border-b bg-background/70 backdrop-blur", children: _jsxs("div", { className: "flex items-center gap-3 p-4 md:p-5", children: [_jsxs("div", { className: "relative w-full max-w-md", children: [_jsx(Search, { className: "pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" }), _jsx(Input, { className: "pl-9", placeholder: "Search patients, reports, appointments..." })] }), _jsxs("div", { className: "ml-auto flex items-center gap-2", children: [_jsx(Button, { variant: "outline", size: "icon", className: "rounded-xl", children: _jsx(Bell, { className: "h-4 w-4" }) }), _jsxs(DropdownMenu, { children: [_jsx(DropdownMenuTrigger, { asChild: true, children: _jsxs("button", { className: "flex items-center gap-2 rounded-xl border bg-card px-2 py-1.5 hover:bg-muted", children: [_jsx(Avatar, { className: "h-7 w-7", children: _jsx(AvatarFallback, { children: "MF" }) }), _jsx("span", { className: "hidden text-sm md:block", children: "Mohammed" })] }) }), _jsxs(DropdownMenuContent, { align: "end", className: "w-48", children: [_jsx(DropdownMenuItem, { children: "Profile" }), _jsx(DropdownMenuItem, { children: "Team" }), _jsx(DropdownMenuItem, { children: "Sign out" })] })] })] })] }) }));
}
