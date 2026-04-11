import { jsx as _jsx } from "react/jsx-runtime";
import { Outlet } from "react-router-dom";
export default function AuthLayout() {
    return (_jsx("div", { className: "min-h-screen grid place-items-center bg-muted/30 text-foreground px-4", children: _jsx("div", { className: "w-full max-w-md", children: _jsx(Outlet, {}) }) }));
}
