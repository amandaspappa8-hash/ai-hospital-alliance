import { ReactNode } from "react"
import Sidebar from "@/components/Sidebar"
import Topbar from "@/components/Topbar"
import MedicalChatbot from "@/components/MedicalChatbot"
import { ThemeProvider, useTheme } from "@/lib/theme"

function Layout({ children }: { children: ReactNode }) {
  const { theme } = useTheme()
  return (
    <div style={{
      display: "flex", minHeight: "100vh",
      background: theme === "dark" ? "linear-gradient(135deg,#020817,#0f1629)" : "#f1f5f9",
    }}>
      <Sidebar />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <Topbar />
        <main style={{ flex: 1, overflowY: "auto" }}>{children}</main>
      </div>
      <MedicalChatbot />
    </div>
  )
}

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <Layout>{children}</Layout>
    </ThemeProvider>
  )
}
