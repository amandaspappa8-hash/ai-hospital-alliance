import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { Link } from "react-router-dom";
import { useCurrentUser } from "@/hooks/use-current-user";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
export default function Topbar() {
    const user = useCurrentUser();
    return (_jsxs("header", { className: "flex items-center justify-between border-b bg-background px-4 py-3 md:px-6", children: [_jsxs("div", { children: [_jsx("h1", { className: "text-lg font-semibold", children: "AI Hospital Alliance" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Medical-grade hospital workspace" })] }), _jsx("div", { className: "flex items-center gap-3", children: user ? (_jsxs(_Fragment, { children: [_jsxs("div", { className: "hidden text-right sm:block", children: [_jsx("div", { className: "text-sm font-medium", children: user.name }), _jsx("div", { className: "text-xs text-muted-foreground", children: user.username })] }), _jsx(Badge, { variant: "secondary", children: user.role }), _jsx(Link, { to: "/logout", children: _jsx(Button, { variant: "outline", children: "Logout" }) })] })) : (_jsx(Link, { to: "/login", children: _jsx(Button, { children: "Login" }) })) })] }));
}
