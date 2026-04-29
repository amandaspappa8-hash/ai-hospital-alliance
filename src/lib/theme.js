import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useState, useEffect } from "react";
const ThemeContext = createContext({ theme: "dark", toggle: () => { } });
function getSavedTheme() {
    try {
        return localStorage.getItem("aiha_theme") ?? "dark";
    }
    catch {
        return "dark";
    }
}
export function ThemeProvider({ children }) {
    const [theme, setTheme] = useState("dark");
    useEffect(() => {
        setTheme(getSavedTheme());
    }, []);
    useEffect(() => {
        try {
            localStorage.setItem("aiha_theme", theme);
        }
        catch { }
        document.documentElement.setAttribute("data-theme", theme);
        document.body.style.background = theme === "dark" ? "#020817" : "#f1f5f9";
        document.body.style.color = theme === "dark" ? "white" : "#0f172a";
    }, [theme]);
    function toggle() {
        setTheme(t => t === "dark" ? "light" : "dark");
    }
    return (_jsx(ThemeContext.Provider, { value: { theme, toggle }, children: children }));
}
export function useTheme() { return useContext(ThemeContext); }
