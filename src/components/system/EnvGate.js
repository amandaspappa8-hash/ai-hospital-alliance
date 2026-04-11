import { Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { validateFrontendEnv, isProduction } from "@/lib/env";
export default function EnvGate({ children }) {
    const result = validateFrontendEnv();
    if (result.ok) {
        return _jsx(_Fragment, { children: children });
    }
    if (isProduction) {
        return (_jsx("div", { style: {
                minHeight: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "24px",
                background: "#111827",
                color: "#ffffff",
            }, children: _jsxs("div", { style: {
                    width: "100%",
                    maxWidth: "780px",
                    borderRadius: "16px",
                    padding: "24px",
                    background: "rgba(255,255,255,0.06)",
                    border: "1px solid rgba(255,255,255,0.12)",
                }, children: [_jsx("h1", { style: { marginTop: 0 }, children: "Environment Validation Failed" }), _jsx("p", { children: "The application cannot safely start in production." }), _jsx("ul", { children: result.issues.map((issue) => (_jsx("li", { children: issue }, issue))) })] }) }));
    }
    console.warn("[EnvGate] frontend env issues", result.issues);
    return _jsx(_Fragment, { children: children });
}
