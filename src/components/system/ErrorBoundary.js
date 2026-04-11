import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React from "react";
export default class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
        };
    }
    static getDerivedStateFromError(error) {
        return {
            hasError: true,
            error,
        };
    }
    componentDidCatch(error, errorInfo) {
        console.error("[ErrorBoundary] Caught UI error", {
            message: error.message,
            stack: error.stack,
            componentStack: errorInfo.componentStack,
        });
    }
    handleReload = () => {
        window.location.reload();
    };
    render() {
        if (this.state.hasError) {
            return (_jsx("div", { style: {
                    minHeight: "100vh",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    background: "#0b1020",
                    color: "#ffffff",
                    padding: "24px",
                }, children: _jsxs("div", { style: {
                        width: "100%",
                        maxWidth: "720px",
                        borderRadius: "16px",
                        padding: "24px",
                        background: "rgba(255,255,255,0.06)",
                        border: "1px solid rgba(255,255,255,0.12)",
                        boxShadow: "0 10px 40px rgba(0,0,0,0.25)",
                    }, children: [_jsx("h1", { style: { marginTop: 0, marginBottom: "12px", fontSize: "28px" }, children: "System UI Error" }), _jsx("p", { style: { opacity: 0.9, lineHeight: 1.7 }, children: "Something went wrong in the interface. The application caught the error to prevent a full crash." }), _jsx("div", { style: {
                                marginTop: "16px",
                                padding: "12px",
                                borderRadius: "10px",
                                background: "rgba(0,0,0,0.25)",
                                overflowX: "auto",
                                fontFamily: "monospace",
                                fontSize: "14px",
                            }, children: this.state.error?.message || "Unknown UI error" }), _jsxs("div", { style: { marginTop: "18px", display: "flex", gap: "12px", flexWrap: "wrap" }, children: [_jsx("button", { onClick: this.handleReload, style: {
                                        border: "none",
                                        borderRadius: "10px",
                                        padding: "12px 18px",
                                        cursor: "pointer",
                                        fontWeight: 600,
                                    }, children: "Reload App" }), _jsx("button", { onClick: () => history.back(), style: {
                                        border: "1px solid rgba(255,255,255,0.2)",
                                        background: "transparent",
                                        color: "#fff",
                                        borderRadius: "10px",
                                        padding: "12px 18px",
                                        cursor: "pointer",
                                        fontWeight: 600,
                                    }, children: "Go Back" })] })] }) }));
        }
        return this.props.children;
    }
}
