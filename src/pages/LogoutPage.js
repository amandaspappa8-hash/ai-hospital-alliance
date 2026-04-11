import { jsx as _jsx } from "react/jsx-runtime";
import { Navigate } from "react-router-dom";
import { clearAuth } from "@/lib/auth-storage";
export default function LogoutPage() {
    clearAuth();
    return _jsx(Navigate, { to: "/login", replace: true });
}
