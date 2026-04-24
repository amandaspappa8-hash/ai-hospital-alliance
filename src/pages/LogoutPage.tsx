import { useEffect } from "react"
import { clearAuth } from "@/lib/auth-storage"

export default function LogoutPage() {
  useEffect(() => {
    clearAuth()
    setTimeout(() => { window.location.href = "/login" }, 1500)
  }, [])

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", background: "#020817", color: "white", fontFamily: "Inter,Arial,sans-serif", gap: 16 }}>
      <div style={{ fontSize: 48 }}>👋</div>
      <div style={{ fontSize: 20, fontWeight: 700 }}>Logging out...</div>
      <div style={{ color: "#64748b", fontSize: 13 }}>Redirecting to login page</div>
    </div>
  )
}
