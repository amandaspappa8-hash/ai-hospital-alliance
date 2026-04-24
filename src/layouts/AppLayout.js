import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import MedicalChatbot from "@/components/MedicalChatbot";
import { ThemeProvider, useTheme } from "@/lib/theme";
function Layout({ children }) {
    const { theme } = useTheme();
    return (_jsxs("div", { style: {
            display: "flex", minHeight: "100vh",
            background: theme === "dark" ? "linear-gradient(135deg,#020817,#0f1629)" : "#f1f5f9",
        }, children: [_jsx(Sidebar, {}), _jsxs("div", { style: { flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }, children: [_jsx(Topbar, {}), _jsx("main", { style: { flex: 1, overflowY: "auto" }, children: children })] }), _jsx(MedicalChatbot, {})] }));
}
export default function AppLayout({ children }) {
    return (_jsx(ThemeProvider, { children: _jsx(Layout, { children: children }) }));
}
