import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from "react";
export default function PWAInstall() {
    const [prompt, setPrompt] = useState(null);
    const [installed, setInstalled] = useState(false);
    const [show, setShow] = useState(false);
    useEffect(() => {
        // Check if already installed
        if (window.matchMedia("(display-mode: standalone)").matches) {
            setInstalled(true);
            return;
        }
        const handler = (e) => {
            e.preventDefault();
            setPrompt(e);
            // Show banner after 3 seconds
            setTimeout(() => setShow(true), 3000);
        };
        window.addEventListener("beforeinstallprompt", handler);
        window.addEventListener("appinstalled", () => {
            setInstalled(true);
            setShow(false);
        });
        return () => window.removeEventListener("beforeinstallprompt", handler);
    }, []);
    async function install() {
        if (!prompt)
            return;
        await prompt.prompt();
        const { outcome } = await prompt.userChoice;
        if (outcome === "accepted") {
            setInstalled(true);
            setShow(false);
        }
    }
    if (!show || installed || !prompt)
        return null;
    return (_jsxs("div", { style: {
            position: "fixed", bottom: 20, left: "50%", transform: "translateX(-50%)",
            zIndex: 9999, width: "calc(100% - 40px)", maxWidth: 420,
            background: "linear-gradient(135deg,#0f172a,#1e3a5f)",
            border: "1px solid rgba(59,130,246,0.4)",
            borderRadius: 16, padding: "16px 20px",
            boxShadow: "0 20px 60px rgba(0,0,0,0.6), 0 0 40px rgba(59,130,246,0.2)",
            display: "flex", alignItems: "center", gap: 14,
            animation: "slideUp 0.3s ease",
        }, children: [_jsx("style", { children: `
        @keyframes slideUp {
          from { transform: translateX(-50%) translateY(100px); opacity: 0; }
          to   { transform: translateX(-50%) translateY(0); opacity: 1; }
        }
      ` }), _jsx("div", { style: {
                    width: 48, height: 48, borderRadius: 12, flexShrink: 0,
                    background: "linear-gradient(135deg,#2563eb,#7c3aed)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 24, boxShadow: "0 0 20px rgba(37,99,235,0.5)",
                }, children: "\uD83C\uDFE5" }), _jsxs("div", { style: { flex: 1, minWidth: 0 }, children: [_jsx("div", { style: { fontWeight: 800, color: "white", fontSize: 14, marginBottom: 2 }, children: "Install AI Hospital Alliance" }), _jsx("div", { style: { color: "#94a3b8", fontSize: 11, lineHeight: 1.4 }, children: "Add to home screen for quick access \u00B7 Works offline" })] }), _jsxs("div", { style: { display: "flex", gap: 8, flexShrink: 0 }, children: [_jsx("button", { onClick: () => setShow(false), style: {
                            padding: "8px 12px", borderRadius: 8, fontSize: 12, fontWeight: 600,
                            background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)",
                            color: "#64748b", cursor: "pointer",
                        }, children: "Later" }), _jsx("button", { onClick: install, style: {
                            padding: "8px 16px", borderRadius: 8, fontSize: 12, fontWeight: 800,
                            background: "linear-gradient(135deg,#2563eb,#7c3aed)",
                            border: "none", color: "white", cursor: "pointer",
                            boxShadow: "0 0 16px rgba(37,99,235,0.4)",
                        }, children: "Install" })] })] }));
}
