import { Fragment as _Fragment, jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { getToken, getUser } from "@/lib/auth-storage";
import { hasAccess } from "@/lib/rbac";
export default function ProtectedRoute({ children, routeKey }) {
    const navigate = useNavigate();
    const location = useLocation();
    const redirected = useRef(false);
    const token = getToken();
    const user = getUser();
    useEffect(() => {
        if (redirected.current)
            return;
        if (!token || !user) {
            redirected.current = true;
            navigate("/login", { replace: true, state: { from: location } });
        }
        else if (routeKey && !hasAccess(user.role, routeKey)) {
            redirected.current = true;
            navigate("/dashboard", { replace: true });
        }
    }, [token]);
    if (!token || !user)
        return null;
    return _jsx(_Fragment, { children: children });
}
