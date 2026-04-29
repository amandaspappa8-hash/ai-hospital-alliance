import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useMemo } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { clearAuth, getToken, saveAuth } from "@/lib/auth-storage";
import { login } from "@/services/auth";
export default function Login() {
    // useMemo يمنع إعادة قراءة localStorage عند كل render
    const existingToken = useMemo(() => getToken(), []);
    const navigate = useNavigate();
    const [username, setUsername] = useState("admin");
    const [password, setPassword] = useState("admin123");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    // إذا كان مسجلاً مسبقاً، وجّهه مباشرة
    if (existingToken)
        return _jsx(Navigate, { to: "/dashboard", replace: true });
    async function handleLogin(e) {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
            clearAuth();
            const data = await login(username.trim(), password.trim());
            saveAuth(data.access_token, data.user);
            // navigate بدلاً من window.location لتجنب إعادة mount كاملة
            navigate("/dashboard", { replace: true });
        }
        catch (err) {
            setError(err instanceof Error ? err.message : "Login failed");
        }
        finally {
            setLoading(false);
        }
    }
    return (_jsx("div", { style: { minHeight: "100vh", display: "grid", placeItems: "center", background: "#030712", color: "white", padding: 24 }, children: _jsxs("form", { onSubmit: handleLogin, style: { width: "100%", maxWidth: 420, background: "#111827", border: "1px solid #374151", borderRadius: 16, padding: 24 }, children: [_jsx("h1", { style: { fontSize: 28, marginBottom: 8 }, children: "AI Hospital Alliance" }), _jsx("p", { style: { opacity: 0.8, marginBottom: 20 }, children: "Medical platform login" }), _jsx("label", { children: "Username" }), _jsx("input", { value: username, onChange: (e) => setUsername(e.target.value), style: s }), _jsx("label", { style: { marginTop: 12, display: "block" }, children: "Password" }), _jsx("input", { type: "password", value: password, onChange: (e) => setPassword(e.target.value), style: s }), _jsx("button", { type: "submit", disabled: loading, style: { width: "100%", padding: 12, marginTop: 16, borderRadius: 10 }, children: loading ? "Signing in..." : "Login" }), error && _jsx("div", { style: { color: "#fca5a5", marginTop: 14 }, children: error })] }) }));
}
const s = {
    width: "100%",
    padding: "10px 12px",
    marginTop: 6,
    borderRadius: 10,
    border: "1px solid #374151",
    background: "#030712",
    color: "white",
};
