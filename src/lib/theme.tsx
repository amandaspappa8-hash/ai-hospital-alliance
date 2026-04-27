import { createContext, useContext, useState, useEffect, ReactNode } from "react"

type Theme = "dark" | "light"
type ThemeCtx = { theme: Theme; toggle: () => void }

const ThemeContext = createContext<ThemeCtx>({ theme: "dark", toggle: () => {} })

function getSavedTheme(): Theme {
  try { return (localStorage.getItem("aiha_theme") as Theme) ?? "dark" } catch { return "dark" }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("dark")

  useEffect(() => {
    setTheme(getSavedTheme())
  }, [])

  useEffect(() => {
    try { localStorage.setItem("aiha_theme", theme) } catch {}
    document.documentElement.setAttribute("data-theme", theme)
    document.body.style.background = theme === "dark" ? "#020817" : "#f1f5f9"
    document.body.style.color = theme === "dark" ? "white" : "#0f172a"
  }, [theme])

  function toggle() {
    setTheme(t => t === "dark" ? "light" : "dark")
  }

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() { return useContext(ThemeContext) }
