import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { Navigate } from "react-router-dom";
import { getToken, getUser } from "@/lib/auth-storage";
import { hasAccess } from "@/lib/rbac";
export default function ProtectedRoute({ children, routeKey }) {
    const token = getToken();
    const user = getUser();
    if (!token || !user) {
        return _jsx(Navigate, { to: "/login", replace: true });
    }
    if (routeKey && !hasAccess(user.role, routeKey)) {
        return _jsx(Navigate, { to: "/dashboard", replace: true });
    }
    return _jsx(_Fragment, { children: children });
}
