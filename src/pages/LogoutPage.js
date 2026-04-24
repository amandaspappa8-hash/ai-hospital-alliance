import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect } from "react";
import { clearAuth } from "@/lib/auth-storage";
export default function LogoutPage() {
    useEffect(() => {
        clearAuth();
        setTimeout(() => { window.location.href = "/login"; }, 1500);
    }, []);
    return (_jsxs("div", { style: { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020817", color: "white", fontFamily: "Inter,Arial,sans-serif", gap: 16 }, children: [_jsx("div", { style: { fontSize: 48 }, children: "\uD83D\uDC4B" }), _jsx("div", { style: { fontSize: 20, fontWeight: 700 }, children: "Logging out..." }), _jsx("div", { style: { color: "#64748b", fontSize: 13 }, children: "Redirecting to login page" })] }));
}
