import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
export default function Login() {
    return (_jsx("div", { className: "min-h-screen bg-background flex items-center justify-center p-4", children: _jsxs(Card, { className: "w-full max-w-md", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { children: "Sign in" }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsx(Input, { placeholder: "Email" }), _jsx(Input, { placeholder: "Password", type: "password" }), _jsx(Button, { className: "w-full", children: "Login" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "(Demo UI only \u2014 backend later)" })] })] }) }));
}
