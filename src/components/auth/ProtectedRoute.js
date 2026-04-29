import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { useMemo } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { getToken, getUser } from "@/lib/auth-storage";
import { hasAccess } from "@/lib/rbac";
export default function ProtectedRoute({ children, routeKey }) {
    const location = useLocation();
    const token = useMemo(() => getToken(), []);
    const user = useMemo(() => getUser(), []);
    if (!token || !user) {
        return _jsx(Navigate, { to: "/login", replace: true, state: { from: location } });
    }
    if (routeKey && !hasAccess(user.role, routeKey)) {
        return _jsx(Navigate, { to: "/dashboard", replace: true });
    }
    return _jsx(_Fragment, { children: children });
}
